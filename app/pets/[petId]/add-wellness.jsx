import React, { useState } from 'react';
import { ScrollView, StyleSheet, View, Alert } from 'react-native';
import {
  TextInput,
  Button,
  Text,
  Title,
  Card,
  HelperText,
} from 'react-native-paper';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useRouter, useLocalSearchParams } from 'expo-router';
import { petService } from '../../../src/services/supabase';

export default function AddWellnessScreen() {
  const router = useRouter();
  const { petId } = useLocalSearchParams();
  const [loading, setLoading] = useState(false);

  const [formData, setFormData] = useState({
    fecha: new Date().toISOString().split('T')[0],
    peso: '',
    altura: '',
    actividad: '',
    horas_descanso: '',
    temperatura: '',
    notas: '',
  });

  const [errors, setErrors] = useState({});

  const validateForm = () => {
    const newErrors = {};

    if (!formData.fecha) {
      newErrors.fecha = 'La fecha es requerida';
    }

    // Al menos peso o alguna otra métrica debe estar presente
    if (!formData.peso && !formData.actividad && !formData.horas_descanso && !formData.temperatura) {
      newErrors.peso = 'Debes registrar al menos una métrica (peso, actividad, descanso o temperatura)';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSave = async () => {
    if (!validateForm()) {
      Alert.alert('Error', 'Por favor completa al menos una métrica');
      return;
    }

    setLoading(true);

    try {
      const indicatorData = {
        fecha: formData.fecha,
        peso: formData.peso ? parseFloat(formData.peso) : null,
        altura: formData.altura ? parseFloat(formData.altura) : null,
        actividad: formData.actividad ? parseInt(formData.actividad) : null,
        horas_descanso: formData.horas_descanso ? parseFloat(formData.horas_descanso) : null,
        temperatura: formData.temperatura ? parseFloat(formData.temperatura) : null,
        notas: formData.notas.trim() || null,
      };

      const { data, error } = await petService.addWellnessIndicator(petId, indicatorData);

      if (error) {
        throw error;
      }

      Alert.alert('¡Éxito!', 'Indicador de bienestar registrado correctamente', [
        {
          text: 'OK',
          onPress: () => router.back(),
        },
      ]);
    } catch (error) {
      console.error('Error agregando indicador:', error);
      Alert.alert(
        'Error',
        `No se pudo registrar el indicador: ${error.message || error}`
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView style={styles.scrollView} contentContainerStyle={styles.scrollContent}>
        <Title style={styles.title}>Registrar Indicador de Bienestar</Title>

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
            <HelperText type="info">Fecha del registro</HelperText>
          </Card.Content>
        </Card>

        {/* Peso */}
        <Card style={styles.card}>
          <Card.Content>
            <TextInput
              label="Peso (kg)"
              value={formData.peso}
              onChangeText={(text) => setFormData({ ...formData, peso: text })}
              mode="outlined"
              keyboardType="decimal-pad"
              style={styles.input}
              placeholder="0.0"
              error={!!errors.peso}
              right={<TextInput.Affix text="kg" />}
            />
            {errors.peso && <HelperText type="error">{errors.peso}</HelperText>}
            <HelperText type="info">Peso actual de la mascota</HelperText>
          </Card.Content>
        </Card>

        {/* Altura */}
        <Card style={styles.card}>
          <Card.Content>
            <TextInput
              label="Altura (cm)"
              value={formData.altura}
              onChangeText={(text) => setFormData({ ...formData, altura: text })}
              mode="outlined"
              keyboardType="decimal-pad"
              style={styles.input}
              placeholder="0.0"
              right={<TextInput.Affix text="cm" />}
            />
            <HelperText type="info">Altura a la cruz (opcional)</HelperText>
          </Card.Content>
        </Card>

        {/* Actividad */}
        <Card style={styles.card}>
          <Card.Content>
            <TextInput
              label="Actividad (minutos)"
              value={formData.actividad}
              onChangeText={(text) => setFormData({ ...formData, actividad: text })}
              mode="outlined"
              keyboardType="number-pad"
              style={styles.input}
              placeholder="0"
              right={<TextInput.Affix text="min" />}
            />
            <HelperText type="info">Minutos de actividad o pasos del día (opcional)</HelperText>
          </Card.Content>
        </Card>

        {/* Horas de descanso */}
        <Card style={styles.card}>
          <Card.Content>
            <TextInput
              label="Horas de descanso"
              value={formData.horas_descanso}
              onChangeText={(text) => setFormData({ ...formData, horas_descanso: text })}
              mode="outlined"
              keyboardType="decimal-pad"
              style={styles.input}
              placeholder="0.0"
              right={<TextInput.Affix text="hrs" />}
            />
            <HelperText type="info">Horas de sueño/descanso del día (opcional)</HelperText>
          </Card.Content>
        </Card>

        {/* Temperatura */}
        <Card style={styles.card}>
          <Card.Content>
            <TextInput
              label="Temperatura (°C)"
              value={formData.temperatura}
              onChangeText={(text) => setFormData({ ...formData, temperatura: text })}
              mode="outlined"
              keyboardType="decimal-pad"
              style={styles.input}
              placeholder="0.0"
              right={<TextInput.Affix text="°C" />}
            />
            <HelperText type="info">Temperatura corporal (opcional)</HelperText>
          </Card.Content>
        </Card>

        {/* Notas */}
        <Card style={styles.card}>
          <Card.Content>
            <TextInput
              label="Notas"
              value={formData.notas}
              onChangeText={(text) => setFormData({ ...formData, notas: text })}
              mode="outlined"
              multiline
              numberOfLines={3}
              style={styles.input}
              placeholder="Observaciones adicionales..."
            />
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
            Guardar Indicador
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

