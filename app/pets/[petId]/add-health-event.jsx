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

export default function AddHealthEventScreen() {
  const router = useRouter();
  const { petId } = useLocalSearchParams();
  const [loading, setLoading] = useState(false);

  const [formData, setFormData] = useState({
    tipo_evento: 'chequeo',
    fecha: new Date().toISOString().split('T')[0],
    descripcion: '',
    veterinario: '',
    notas: '',
    costo: '',
  });

  const [errors, setErrors] = useState({});

  const validateForm = () => {
    const newErrors = {};

    if (!formData.descripcion.trim()) {
      newErrors.descripcion = 'La descripción es requerida';
    }

    if (!formData.fecha) {
      newErrors.fecha = 'La fecha es requerida';
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
      const eventData = {
        tipo_evento: formData.tipo_evento,
        fecha: formData.fecha,
        descripcion: formData.descripcion.trim(),
        veterinario: formData.veterinario.trim() || null,
        notas: formData.notas.trim() || null,
        costo: formData.costo ? parseFloat(formData.costo) : null,
      };

      const { data, error } = await petService.addHealthEvent(petId, eventData);

      if (error) {
        throw error;
      }

      Alert.alert('¡Éxito!', 'Evento de salud registrado correctamente', [
        {
          text: 'OK',
          onPress: () => router.back(),
        },
      ]);
    } catch (error) {
      console.error('Error agregando evento:', error);
      Alert.alert(
        'Error',
        `No se pudo registrar el evento: ${error.message || error}`
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView style={styles.scrollView} contentContainerStyle={styles.scrollContent}>
        <Title style={styles.title}>Agregar Evento de Salud</Title>

        {/* Tipo de evento */}
        <Card style={styles.card}>
          <Card.Content>
            <Text style={styles.label}>Tipo de evento *</Text>
            <View style={styles.radioGroup}>
              <View style={styles.radioOption}>
                <RadioButton
                  value="chequeo"
                  status={formData.tipo_evento === 'chequeo' ? 'checked' : 'unchecked'}
                  onPress={() => setFormData({ ...formData, tipo_evento: 'chequeo' })}
                />
                <Text style={styles.radioLabel}>Chequeo</Text>
              </View>
              <View style={styles.radioOption}>
                <RadioButton
                  value="enfermedad"
                  status={formData.tipo_evento === 'enfermedad' ? 'checked' : 'unchecked'}
                  onPress={() => setFormData({ ...formData, tipo_evento: 'enfermedad' })}
                />
                <Text style={styles.radioLabel}>Enfermedad</Text>
              </View>
              <View style={styles.radioOption}>
                <RadioButton
                  value="cirugia"
                  status={formData.tipo_evento === 'cirugia' ? 'checked' : 'unchecked'}
                  onPress={() => setFormData({ ...formData, tipo_evento: 'cirugia' })}
                />
                <Text style={styles.radioLabel}>Cirugía</Text>
              </View>
              <View style={styles.radioOption}>
                <RadioButton
                  value="alergia"
                  status={formData.tipo_evento === 'alergia' ? 'checked' : 'unchecked'}
                  onPress={() => setFormData({ ...formData, tipo_evento: 'alergia' })}
                />
                <Text style={styles.radioLabel}>Alergia</Text>
              </View>
              <View style={styles.radioOption}>
                <RadioButton
                  value="otro"
                  status={formData.tipo_evento === 'otro' ? 'checked' : 'unchecked'}
                  onPress={() => setFormData({ ...formData, tipo_evento: 'otro' })}
                />
                <Text style={styles.radioLabel}>Otro</Text>
              </View>
            </View>
          </Card.Content>
        </Card>

        {/* Fecha */}
        <Card style={styles.card}>
          <Card.Content>
            <TextInput
              label="Fecha *"
              value={formData.fecha}
              onChangeText={(text) => setFormData({ ...formData, fecha: text })}
              mode="outlined"
              style={styles.input}
              placeholder="YYYY-MM-DD"
              error={!!errors.fecha}
            />
            {errors.fecha && <HelperText type="error">{errors.fecha}</HelperText>}
            <HelperText type="info">Formato: AAAA-MM-DD (ej: 2025-01-15)</HelperText>
          </Card.Content>
        </Card>

        {/* Descripción */}
        <Card style={styles.card}>
          <Card.Content>
            <TextInput
              label="Descripción *"
              value={formData.descripcion}
              onChangeText={(text) => setFormData({ ...formData, descripcion: text })}
              mode="outlined"
              multiline
              numberOfLines={4}
              style={styles.input}
              error={!!errors.descripcion}
              placeholder="Describe el evento de salud..."
            />
            {errors.descripcion && <HelperText type="error">{errors.descripcion}</HelperText>}
          </Card.Content>
        </Card>

        {/* Veterinario */}
        <Card style={styles.card}>
          <Card.Content>
            <TextInput
              label="Veterinario"
              value={formData.veterinario}
              onChangeText={(text) => setFormData({ ...formData, veterinario: text })}
              mode="outlined"
              style={styles.input}
              placeholder="Nombre del veterinario (opcional)"
            />
          </Card.Content>
        </Card>

        {/* Notas */}
        <Card style={styles.card}>
          <Card.Content>
            <TextInput
              label="Notas adicionales"
              value={formData.notas}
              onChangeText={(text) => setFormData({ ...formData, notas: text })}
              mode="outlined"
              multiline
              numberOfLines={3}
              style={styles.input}
              placeholder="Notas adicionales sobre el evento..."
            />
          </Card.Content>
        </Card>

        {/* Costo */}
        <Card style={styles.card}>
          <Card.Content>
            <TextInput
              label="Costo"
              value={formData.costo}
              onChangeText={(text) => setFormData({ ...formData, costo: text })}
              mode="outlined"
              keyboardType="decimal-pad"
              style={styles.input}
              placeholder="0.00"
              left={<TextInput.Affix text="$" />}
            />
            <HelperText type="info">Costo del tratamiento o consulta (opcional)</HelperText>
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
            Guardar Evento
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


