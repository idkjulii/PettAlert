import React, { useState } from 'react';
import { ScrollView, StyleSheet, View, Alert } from 'react-native';
import {
  TextInput,
  Button,
  Text,
  Title,
  Card,
  RadioButton,
  HelperText,
} from 'react-native-paper';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useRouter, useLocalSearchParams } from 'expo-router';
import { petService } from '../../../src/services/supabase';

export default function AddReminderScreen() {
  const router = useRouter();
  const { petId } = useLocalSearchParams();
  const [loading, setLoading] = useState(false);

  const [formData, setFormData] = useState({
    tipo: 'vacuna',
    titulo: '',
    descripcion: '',
    fecha_programada: '',
    hora_programada: '',
    repeticion: 'una_vez',
  });

  const [errors, setErrors] = useState({});

  const validateForm = () => {
    const newErrors = {};

    if (!formData.titulo.trim()) {
      newErrors.titulo = 'El título es requerido';
    }

    if (!formData.fecha_programada) {
      newErrors.fecha_programada = 'La fecha es requerida';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSave = async () => {
    if (!validateForm()) {
      Alert.alert('Error', 'Por favor completa todos los campos requeridos');
      return;
    }

    setLoading(true);

    try {
      const reminderData = {
        tipo: formData.tipo,
        titulo: formData.titulo.trim(),
        descripcion: formData.descripcion.trim() || null,
        fecha_programada: formData.fecha_programada,
        hora_programada: formData.hora_programada || null,
        repeticion: formData.repeticion,
        activo: true,
        cumplido: false,
      };

      const { data, error } = await petService.createReminder(petId, reminderData);

      if (error) {
        throw error;
      }

      Alert.alert('¡Éxito!', 'Recordatorio creado correctamente', [
        {
          text: 'OK',
          onPress: () => router.back(),
        },
      ]);
    } catch (error) {
      console.error('Error creando recordatorio:', error);
      Alert.alert(
        'Error',
        `No se pudo crear el recordatorio: ${error.message || error}`
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView style={styles.scrollView} contentContainerStyle={styles.scrollContent}>
        <Title style={styles.title}>Crear Recordatorio</Title>

        {/* Tipo */}
        <Card style={styles.card}>
          <Card.Content>
            <Text style={styles.label}>Tipo *</Text>
            <View style={styles.radioGroup}>
              <View style={styles.radioOption}>
                <RadioButton
                  value="vacuna"
                  status={formData.tipo === 'vacuna' ? 'checked' : 'unchecked'}
                  onPress={() => setFormData({ ...formData, tipo: 'vacuna' })}
                />
                <Text style={styles.radioLabel}>Vacuna</Text>
              </View>
              <View style={styles.radioOption}>
                <RadioButton
                  value="chequeo"
                  status={formData.tipo === 'chequeo' ? 'checked' : 'unchecked'}
                  onPress={() => setFormData({ ...formData, tipo: 'chequeo' })}
                />
                <Text style={styles.radioLabel}>Chequeo</Text>
              </View>
              <View style={styles.radioOption}>
                <RadioButton
                  value="medicamento"
                  status={formData.tipo === 'medicamento' ? 'checked' : 'unchecked'}
                  onPress={() => setFormData({ ...formData, tipo: 'medicamento' })}
                />
                <Text style={styles.radioLabel}>Medicamento</Text>
              </View>
              <View style={styles.radioOption}>
                <RadioButton
                  value="desparasitacion"
                  status={formData.tipo === 'desparasitacion' ? 'checked' : 'unchecked'}
                  onPress={() => setFormData({ ...formData, tipo: 'desparasitacion' })}
                />
                <Text style={styles.radioLabel}>Desparasitación</Text>
              </View>
              <View style={styles.radioOption}>
                <RadioButton
                  value="otro"
                  status={formData.tipo === 'otro' ? 'checked' : 'unchecked'}
                  onPress={() => setFormData({ ...formData, tipo: 'otro' })}
                />
                <Text style={styles.radioLabel}>Otro</Text>
              </View>
            </View>
          </Card.Content>
        </Card>

        {/* Título */}
        <Card style={styles.card}>
          <Card.Content>
            <TextInput
              label="Título *"
              value={formData.titulo}
              onChangeText={(text) => setFormData({ ...formData, titulo: text })}
              mode="outlined"
              style={styles.input}
              error={!!errors.titulo}
              placeholder="Ej: Vacuna antirrábica, Chequeo anual..."
            />
            {errors.titulo && <HelperText type="error">{errors.titulo}</HelperText>}
          </Card.Content>
        </Card>

        {/* Descripción */}
        <Card style={styles.card}>
          <Card.Content>
            <TextInput
              label="Descripción"
              value={formData.descripcion}
              onChangeText={(text) => setFormData({ ...formData, descripcion: text })}
              mode="outlined"
              multiline
              numberOfLines={3}
              style={styles.input}
              placeholder="Detalles adicionales del recordatorio..."
            />
          </Card.Content>
        </Card>

        {/* Fecha programada */}
        <Card style={styles.card}>
          <Card.Content>
            <TextInput
              label="Fecha programada *"
              value={formData.fecha_programada}
              onChangeText={(text) => setFormData({ ...formData, fecha_programada: text })}
              mode="outlined"
              style={styles.input}
              placeholder="YYYY-MM-DD"
              error={!!errors.fecha_programada}
            />
            {errors.fecha_programada && <HelperText type="error">{errors.fecha_programada}</HelperText>}
            <HelperText type="info">Fecha en que debe cumplirse el recordatorio</HelperText>
          </Card.Content>
        </Card>

        {/* Hora programada */}
        <Card style={styles.card}>
          <Card.Content>
            <TextInput
              label="Hora programada"
              value={formData.hora_programada}
              onChangeText={(text) => setFormData({ ...formData, hora_programada: text })}
              mode="outlined"
              style={styles.input}
              placeholder="HH:MM (ej: 09:00)"
            />
            <HelperText type="info">Hora específica (opcional, formato 24h)</HelperText>
          </Card.Content>
        </Card>

        {/* Repetición */}
        <Card style={styles.card}>
          <Card.Content>
            <Text style={styles.label}>Repetición</Text>
            <View style={styles.radioGroup}>
              <View style={styles.radioOption}>
                <RadioButton
                  value="una_vez"
                  status={formData.repeticion === 'una_vez' ? 'checked' : 'unchecked'}
                  onPress={() => setFormData({ ...formData, repeticion: 'una_vez' })}
                />
                <Text style={styles.radioLabel}>Una vez</Text>
              </View>
              <View style={styles.radioOption}>
                <RadioButton
                  value="diario"
                  status={formData.repeticion === 'diario' ? 'checked' : 'unchecked'}
                  onPress={() => setFormData({ ...formData, repeticion: 'diario' })}
                />
                <Text style={styles.radioLabel}>Diario</Text>
              </View>
              <View style={styles.radioOption}>
                <RadioButton
                  value="semanal"
                  status={formData.repeticion === 'semanal' ? 'checked' : 'unchecked'}
                  onPress={() => setFormData({ ...formData, repeticion: 'semanal' })}
                />
                <Text style={styles.radioLabel}>Semanal</Text>
              </View>
              <View style={styles.radioOption}>
                <RadioButton
                  value="mensual"
                  status={formData.repeticion === 'mensual' ? 'checked' : 'unchecked'}
                  onPress={() => setFormData({ ...formData, repeticion: 'mensual' })}
                />
                <Text style={styles.radioLabel}>Mensual</Text>
              </View>
              <View style={styles.radioOption}>
                <RadioButton
                  value="anual"
                  status={formData.repeticion === 'anual' ? 'checked' : 'unchecked'}
                  onPress={() => setFormData({ ...formData, repeticion: 'anual' })}
                />
                <Text style={styles.radioLabel}>Anual</Text>
              </View>
            </View>
          </Card.Content>
        </Card>

        {/* Botones */}
        <View style={styles.actions}>
          <Button
            mode="outlined"
            onPress={() => router.back()}
            style={styles.cancelButton}
            disabled={loading}
          >
            Cancelar
          </Button>
          <Button
            mode="contained"
            onPress={handleSave}
            loading={loading}
            disabled={loading}
            style={styles.saveButton}
          >
            Crear Recordatorio
          </Button>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  scrollView: {
    flex: 1,
  },
  scrollContent: {
    padding: 16,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 20,
    textAlign: 'center',
  },
  card: {
    marginBottom: 16,
    elevation: 2,
  },
  input: {
    marginBottom: 8,
  },
  label: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
    marginBottom: 12,
  },
  radioGroup: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 8,
  },
  radioOption: {
    flexDirection: 'row',
    alignItems: 'center',
    marginRight: 16,
    marginBottom: 8,
  },
  radioLabel: {
    marginLeft: 8,
    fontSize: 16,
  },
  actions: {
    flexDirection: 'row',
    gap: 12,
    marginTop: 24,
    marginBottom: 32,
  },
  cancelButton: {
    flex: 1,
  },
  saveButton: {
    flex: 2,
  },
});

