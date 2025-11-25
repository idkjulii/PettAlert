import React, { useState } from 'react';
import {
  ScrollView,
  StyleSheet,
  View,
  Alert,
  Image,
  TouchableOpacity,
} from 'react-native';
import {
  TextInput,
  Button,
  Text,
  Title,
  Card,
  ActivityIndicator,
  RadioButton,
  HelperText,
} from 'react-native-paper';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useRouter } from 'expo-router';
import * as ImagePicker from 'expo-image-picker';
import { petService } from '../../src/services/supabase';
import { useAuthStore } from '../../src/stores/authStore';
import { storageService } from '../../src/services/storage';

export default function CreatePetScreen() {
  const router = useRouter();
  const { getUserId } = useAuthStore();
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);

  // Estado del formulario
  const [formData, setFormData] = useState({
    name: '',
    species: 'dog',
    breed: '',
    color: '',
    size: '',
    description: '',
    distinctive_features: '',
    photos: [],
  });

  const [errors, setErrors] = useState({});

  // Validar formulario
  const validateForm = () => {
    const newErrors = {};

    if (!formData.name.trim()) {
      newErrors.name = 'El nombre es requerido';
    }

    if (!formData.species) {
      newErrors.species = 'La especie es requerida';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  // Seleccionar foto desde galería
  const pickImage = async () => {
    try {
      const { status } = await ImagePicker.requestMediaLibraryPermissionsAsync();
      if (status !== 'granted') {
        Alert.alert(
          'Permisos necesarios',
          'Necesitamos acceso a tu galería para agregar fotos de tu mascota.'
        );
        return;
      }

      const result = await ImagePicker.launchImageLibraryAsync({
        mediaTypes: ImagePicker.MediaTypeOptions.Images,
        allowsMultipleSelection: true,
        quality: 0.8,
        allowsEditing: true,
      });

      if (!result.canceled && result.assets) {
        const newPhotos = result.assets.map((asset) => asset.uri);
        setFormData({
          ...formData,
          photos: [...formData.photos, ...newPhotos],
        });
      }
    } catch (error) {
      console.error('Error seleccionando imagen:', error);
      Alert.alert('Error', 'No se pudo seleccionar la imagen');
    }
  };

  // Tomar foto con cámara
  const takePhoto = async () => {
    try {
      const { status } = await ImagePicker.requestCameraPermissionsAsync();
      if (status !== 'granted') {
        Alert.alert(
          'Permisos necesarios',
          'Necesitamos acceso a tu cámara para tomar fotos de tu mascota.'
        );
        return;
      }

      const result = await ImagePicker.launchCameraAsync({
        mediaTypes: ImagePicker.MediaTypeOptions.Images,
        quality: 0.8,
        allowsEditing: true,
      });

      if (!result.canceled && result.assets && result.assets[0]) {
        setFormData({
          ...formData,
          photos: [...formData.photos, result.assets[0].uri],
        });
      }
    } catch (error) {
      console.error('Error tomando foto:', error);
      Alert.alert('Error', 'No se pudo tomar la foto');
    }
  };

  // Eliminar foto
  const removePhoto = (index) => {
    const newPhotos = formData.photos.filter((_, i) => i !== index);
    setFormData({ ...formData, photos: newPhotos });
  };

  // Subir fotos a storage
  const uploadPhotos = async (userId, petId) => {
    if (formData.photos.length === 0) return [];

    setUploading(true);
    let uploadedUrls = [];

    try {
      const { urls, error } = await storageService.uploadPetPhotos(
        userId,
        petId,
        formData.photos
      );

      if (error) {
        console.error('Error subiendo fotos:', error);
        // Continuar aunque haya error, al menos la mascota se creará
      } else {
        uploadedUrls = urls || [];
      }
    } catch (error) {
      console.error('Error en uploadPhotos:', error);
    } finally {
      setUploading(false);
    }

    return uploadedUrls;
  };

  // Guardar mascota
  const handleSave = async () => {
    if (!validateForm()) {
      Alert.alert('Error', 'Por favor completa todos los campos requeridos');
      return;
    }

    const userId = getUserId();
    if (!userId) {
      Alert.alert('Error', 'Debes estar autenticado para crear una mascota');
      router.back();
      return;
    }

    setLoading(true);

    try {
      // Preparar datos
      const petData = {
        owner_id: userId,
        name: formData.name.trim(),
        species: formData.species,
        breed: formData.breed.trim() || null,
        color: formData.color.trim() || null,
        size: formData.size || null,
        description: formData.description.trim() || null,
        distinctive_features: formData.distinctive_features.trim() || null,
        photos: [], // Se actualizará después de subir
        is_lost: false,
      };

      // Crear la mascota primero
      const { data: pet, error: createError } = await petService.createPet(petData);

      if (createError) {
        throw createError;
      }

      // Subir fotos si hay
      if (formData.photos.length > 0) {
        const uploadedUrls = await uploadPhotos(userId, pet.id);
        
        // Actualizar mascota con URLs de fotos
        if (uploadedUrls.length > 0) {
          const { error: updateError } = await petService.updatePet(pet.id, { photos: uploadedUrls });
          if (updateError) {
            console.error('Error actualizando fotos:', updateError);
          }
        }
      }

      Alert.alert(
        '¡Éxito!',
        'Tu mascota ha sido registrada correctamente',
        [
          {
            text: 'Ver Detalle',
            onPress: () => router.replace(`/pets/${pet.id}`),
          },
          {
            text: 'Volver',
            onPress: () => router.back(),
          },
        ]
      );
    } catch (error) {
      console.error('Error creando mascota:', error);
      Alert.alert(
        'Error',
        `No se pudo registrar la mascota: ${error.message || error}`
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView style={styles.scrollView} contentContainerStyle={styles.scrollContent}>
        <Title style={styles.title}>Registrar Nueva Mascota</Title>

        {/* Nombre */}
        <Card style={styles.card}>
          <Card.Content>
            <TextInput
              label="Nombre de la mascota *"
              value={formData.name}
              onChangeText={(text) => setFormData({ ...formData, name: text })}
              error={!!errors.name}
              mode="outlined"
              style={styles.input}
            />
            {errors.name && <HelperText type="error">{errors.name}</HelperText>}
          </Card.Content>
        </Card>

        {/* Especie */}
        <Card style={styles.card}>
          <Card.Content>
            <Text style={styles.label}>Especie *</Text>
            <View style={styles.radioGroup}>
              <View style={styles.radioOption}>
                <RadioButton
                  value="dog"
                  status={formData.species === 'dog' ? 'checked' : 'unchecked'}
                  onPress={() => setFormData({ ...formData, species: 'dog' })}
                />
                <Text style={styles.radioLabel}>🐕 Perro</Text>
              </View>
              <View style={styles.radioOption}>
                <RadioButton
                  value="cat"
                  status={formData.species === 'cat' ? 'checked' : 'unchecked'}
                  onPress={() => setFormData({ ...formData, species: 'cat' })}
                />
                <Text style={styles.radioLabel}>🐱 Gato</Text>
              </View>
              <View style={styles.radioOption}>
                <RadioButton
                  value="bird"
                  status={formData.species === 'bird' ? 'checked' : 'unchecked'}
                  onPress={() => setFormData({ ...formData, species: 'bird' })}
                />
                <Text style={styles.radioLabel}>🐦 Ave</Text>
              </View>
              <View style={styles.radioOption}>
                <RadioButton
                  value="rabbit"
                  status={formData.species === 'rabbit' ? 'checked' : 'unchecked'}
                  onPress={() => setFormData({ ...formData, species: 'rabbit' })}
                />
                <Text style={styles.radioLabel}>🐰 Conejo</Text>
              </View>
              <View style={styles.radioOption}>
                <RadioButton
                  value="other"
                  status={formData.species === 'other' ? 'checked' : 'unchecked'}
                  onPress={() => setFormData({ ...formData, species: 'other' })}
                />
                <Text style={styles.radioLabel}>🐾 Otro</Text>
              </View>
            </View>
          </Card.Content>
        </Card>

        {/* Raza */}
        <Card style={styles.card}>
          <Card.Content>
            <TextInput
              label="Raza"
              value={formData.breed}
              onChangeText={(text) => setFormData({ ...formData, breed: text })}
              mode="outlined"
              style={styles.input}
            />
          </Card.Content>
        </Card>

        {/* Color */}
        <Card style={styles.card}>
          <Card.Content>
            <TextInput
              label="Color"
              value={formData.color}
              onChangeText={(text) => setFormData({ ...formData, color: text })}
              mode="outlined"
              style={styles.input}
            />
          </Card.Content>
        </Card>

        {/* Tamaño */}
        <Card style={styles.card}>
          <Card.Content>
            <Text style={styles.label}>Tamaño (opcional)</Text>
            <View style={styles.radioGroup}>
              <TouchableOpacity 
                style={styles.radioOptionTouchable}
                onPress={() => setFormData({ ...formData, size: 'small' })}
              >
                <View style={styles.radioOption}>
                  <RadioButton
                    value="small"
                    status={formData.size === 'small' ? 'checked' : 'unchecked'}
                    onPress={() => setFormData({ ...formData, size: 'small' })}
                  />
                  <Text style={styles.radioLabel}>Pequeño</Text>
                </View>
              </TouchableOpacity>
              <TouchableOpacity 
                style={styles.radioOptionTouchable}
                onPress={() => setFormData({ ...formData, size: 'medium' })}
              >
                <View style={styles.radioOption}>
                  <RadioButton
                    value="medium"
                    status={formData.size === 'medium' ? 'checked' : 'unchecked'}
                    onPress={() => setFormData({ ...formData, size: 'medium' })}
                  />
                  <Text style={styles.radioLabel}>Mediano</Text>
                </View>
              </TouchableOpacity>
              <TouchableOpacity 
                style={styles.radioOptionTouchable}
                onPress={() => setFormData({ ...formData, size: 'large' })}
              >
                <View style={styles.radioOption}>
                  <RadioButton
                    value="large"
                    status={formData.size === 'large' ? 'checked' : 'unchecked'}
                    onPress={() => setFormData({ ...formData, size: 'large' })}
                  />
                  <Text style={styles.radioLabel}>Grande</Text>
                </View>
              </TouchableOpacity>
            </View>
          </Card.Content>
        </Card>

        {/* Descripción */}
        <Card style={styles.card}>
          <Card.Content>
            <TextInput
              label="Descripción"
              value={formData.description}
              onChangeText={(text) => setFormData({ ...formData, description: text })}
              mode="outlined"
              multiline
              numberOfLines={4}
              style={styles.input}
              placeholder="Describe a tu mascota..."
            />
          </Card.Content>
        </Card>

        {/* Señales particulares */}
        <Card style={styles.card}>
          <Card.Content>
            <TextInput
              label="Señales particulares"
              value={formData.distinctive_features}
              onChangeText={(text) => setFormData({ ...formData, distinctive_features: text })}
              mode="outlined"
              multiline
              numberOfLines={3}
              style={styles.input}
              placeholder="Ej: Mancha blanca en el pecho, cicatriz en la pata..."
            />
          </Card.Content>
        </Card>

        {/* Fotos */}
        <Card style={styles.card}>
          <Card.Content>
            <Text style={styles.label}>Fotos ({formData.photos.length})</Text>
            <View style={styles.photoButtons}>
              <Button
                mode="outlined"
                icon="image"
                onPress={pickImage}
                style={styles.photoButton}
              >
                Galería
              </Button>
              <Button
                mode="outlined"
                icon="camera"
                onPress={takePhoto}
                style={styles.photoButton}
              >
                Cámara
              </Button>
            </View>

            {/* Vista previa de fotos */}
            {formData.photos.length > 0 && (
              <View style={styles.photosContainer}>
                {formData.photos.map((uri, index) => (
                  <View key={index} style={styles.photoPreview}>
                    <Image source={{ uri }} style={styles.photoImage} />
                    <Button
                      mode="text"
                      icon="close"
                      onPress={() => removePhoto(index)}
                      style={styles.removePhotoButton}
                    >
                      Eliminar
                    </Button>
                  </View>
                ))}
              </View>
            )}
          </Card.Content>
        </Card>

        {/* Botones de acción */}
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
            loading={loading || uploading}
            disabled={loading || uploading}
            style={styles.saveButton}
          >
            {uploading ? 'Subiendo fotos...' : loading ? 'Guardando...' : 'Registrar Mascota'}
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
  radioOptionTouchable: {
    marginRight: 16,
    marginBottom: 8,
  },
  radioOption: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  radioLabel: {
    marginLeft: 8,
    fontSize: 16,
  },
  photoButtons: {
    flexDirection: 'row',
    gap: 12,
    marginBottom: 16,
  },
  photoButton: {
    flex: 1,
  },
  photosContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 12,
    marginTop: 12,
  },
  photoPreview: {
    width: 100,
    marginBottom: 8,
  },
  photoImage: {
    width: 100,
    height: 100,
    borderRadius: 8,
    marginBottom: 4,
  },
  removePhotoButton: {
    marginTop: 4,
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

