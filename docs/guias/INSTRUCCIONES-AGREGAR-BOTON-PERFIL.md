# 🔘 Cómo Agregar el Botón de Alertas Geográficas en el Perfil

## Opción 1: Código Completo del Botón

Agrega este código en `app/(tabs)/profile.jsx` donde quieras que aparezca el botón:

```jsx
import { useRouter } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';

// Dentro de tu componente Profile:
const router = useRouter();

// ... resto de tu código ...

// Agregar este botón en la sección de configuración:
<TouchableOpacity 
  style={styles.settingItem}
  onPress={() => router.push('/geo-alerts-settings')}
>
  <View style={styles.settingIcon}>
    <Ionicons name="location" size={24} color="#007AFF" />
  </View>
  <View style={styles.settingContent}>
    <Text style={styles.settingTitle}>Alertas Geográficas</Text>
    <Text style={styles.settingSubtitle}>
      Recibe notificaciones de mascotas cerca de ti
    </Text>
  </View>
  <Ionicons name="chevron-forward" size={20} color="#999" />
</TouchableOpacity>
```

## Opción 2: Estilos Sugeridos

Si no tienes estilos definidos, agrega estos en tu StyleSheet:

```jsx
const styles = StyleSheet.create({
  // ... tus estilos existentes ...
  
  settingItem: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#FFF',
    padding: 16,
    marginHorizontal: 16,
    marginVertical: 4,
    borderRadius: 12,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 2,
    elevation: 2,
  },
  settingIcon: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: '#F0F9FF',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
  },
  settingContent: {
    flex: 1,
  },
  settingTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#000',
    marginBottom: 2,
  },
  settingSubtitle: {
    fontSize: 13,
    color: '#666',
  },
});
```

## Opción 3: Versión Minimalista

Si prefieres un botón más simple:

```jsx
<TouchableOpacity 
  style={styles.menuButton}
  onPress={() => router.push('/geo-alerts-settings')}
>
  <Ionicons name="location" size={22} color="#007AFF" />
  <Text style={styles.menuText}>Alertas Geográficas</Text>
  <Ionicons name="chevron-forward" size={18} color="#CCC" />
</TouchableOpacity>
```

Estilos minimalistas:

```jsx
menuButton: {
  flexDirection: 'row',
  alignItems: 'center',
  padding: 16,
  borderBottomWidth: 1,
  borderBottomColor: '#E5E5E5',
  backgroundColor: '#FFF',
},
menuText: {
  flex: 1,
  fontSize: 16,
  color: '#000',
  marginLeft: 12,
},
```

## Opción 4: Con Badge (indica si está activo)

```jsx
import { useGeoAlerts } from '../../hooks/useGeoAlerts';

// Dentro del componente:
const { locationEnabled } = useGeoAlerts();

<TouchableOpacity 
  style={styles.settingItem}
  onPress={() => router.push('/geo-alerts-settings')}
>
  <View style={styles.settingIcon}>
    <Ionicons name="location" size={24} color="#007AFF" />
  </View>
  <View style={styles.settingContent}>
    <View style={styles.titleRow}>
      <Text style={styles.settingTitle}>Alertas Geográficas</Text>
      {locationEnabled && (
        <View style={styles.activeBadge}>
          <Text style={styles.activeBadgeText}>Activo</Text>
        </View>
      )}
    </View>
    <Text style={styles.settingSubtitle}>
      Recibe notificaciones de mascotas cerca de ti
    </Text>
  </View>
  <Ionicons name="chevron-forward" size={20} color="#999" />
</TouchableOpacity>
```

Estilos adicionales para el badge:

```jsx
titleRow: {
  flexDirection: 'row',
  alignItems: 'center',
  marginBottom: 2,
},
activeBadge: {
  backgroundColor: '#4CAF50',
  paddingHorizontal: 8,
  paddingVertical: 2,
  borderRadius: 10,
  marginLeft: 8,
},
activeBadgeText: {
  fontSize: 11,
  fontWeight: '600',
  color: '#FFF',
},
```

## Ubicación Sugerida en el Perfil

Agrega el botón en una de estas secciones:

### 1. Después de "Editar Perfil":
```jsx
<View style={styles.section}>
  <Text style={styles.sectionTitle}>Configuración</Text>
  
  {/* Botón de Editar Perfil */}
  <TouchableOpacity ...>
    ...
  </TouchableOpacity>
  
  {/* NUEVO: Botón de Alertas Geográficas */}
  <TouchableOpacity 
    style={styles.settingItem}
    onPress={() => router.push('/geo-alerts-settings')}
  >
    ...
  </TouchableOpacity>
  
  {/* Otros botones... */}
</View>
```

### 2. En una sección de "Notificaciones":
```jsx
<View style={styles.section}>
  <Text style={styles.sectionTitle}>Notificaciones</Text>
  
  {/* NUEVO: Botón de Alertas Geográficas */}
  <TouchableOpacity 
    style={styles.settingItem}
    onPress={() => router.push('/geo-alerts-settings')}
  >
    ...
  </TouchableOpacity>
  
  {/* Configuración de notificaciones push */}
  <TouchableOpacity ...>
    ...
  </TouchableOpacity>
</View>
```

### 3. Como ítem destacado al inicio:
```jsx
<ScrollView>
  {/* Header con foto de perfil */}
  ...
  
  {/* NUEVO: Tarjeta destacada de Alertas Geográficas */}
  <View style={styles.featuredCard}>
    <View style={styles.featuredIcon}>
      <Ionicons name="location" size={32} color="#007AFF" />
    </View>
    <View style={styles.featuredContent}>
      <Text style={styles.featuredTitle}>Alertas Geográficas</Text>
      <Text style={styles.featuredSubtitle}>
        Sé el primero en enterarte de mascotas perdidas cerca de ti
      </Text>
    </View>
    <TouchableOpacity 
      style={styles.featuredButton}
      onPress={() => router.push('/geo-alerts-settings')}
    >
      <Text style={styles.featuredButtonText}>Configurar</Text>
    </TouchableOpacity>
  </View>
  
  {/* Resto del perfil */}
  ...
</ScrollView>
```

Estilos para la tarjeta destacada:

```jsx
featuredCard: {
  backgroundColor: '#F0F9FF',
  margin: 16,
  padding: 20,
  borderRadius: 16,
  borderWidth: 2,
  borderColor: '#007AFF',
},
featuredIcon: {
  width: 60,
  height: 60,
  borderRadius: 30,
  backgroundColor: '#FFF',
  justifyContent: 'center',
  alignItems: 'center',
  marginBottom: 12,
},
featuredTitle: {
  fontSize: 20,
  fontWeight: 'bold',
  color: '#000',
  marginBottom: 6,
},
featuredSubtitle: {
  fontSize: 14,
  color: '#666',
  lineHeight: 20,
  marginBottom: 16,
},
featuredButton: {
  backgroundColor: '#007AFF',
  paddingVertical: 12,
  paddingHorizontal: 24,
  borderRadius: 8,
  alignItems: 'center',
},
featuredButtonText: {
  fontSize: 16,
  fontWeight: '600',
  color: '#FFF',
},
```

## Importaciones Necesarias

Asegúrate de tener estas importaciones al inicio del archivo:

```jsx
import { useRouter } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { useGeoAlerts } from '../../hooks/useGeoAlerts'; // Solo si usas el badge
```

## Ejemplo Completo Integrado

```jsx
import React from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  ScrollView,
} from 'react-native';
import { useRouter } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';

export default function ProfileScreen() {
  const router = useRouter();
  
  return (
    <ScrollView style={styles.container}>
      {/* Header con foto de perfil */}
      <View style={styles.header}>
        {/* ... tu código existente ... */}
      </View>
      
      {/* Sección de Configuración */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Configuración</Text>
        
        {/* Botón de Editar Perfil */}
        <TouchableOpacity style={styles.settingItem}>
          <Ionicons name="person-outline" size={24} color="#007AFF" />
          <Text style={styles.settingText}>Editar Perfil</Text>
          <Ionicons name="chevron-forward" size={20} color="#999" />
        </TouchableOpacity>
        
        {/* NUEVO: Alertas Geográficas */}
        <TouchableOpacity 
          style={styles.settingItem}
          onPress={() => router.push('/geo-alerts-settings')}
        >
          <View style={styles.settingIcon}>
            <Ionicons name="location" size={24} color="#007AFF" />
          </View>
          <View style={styles.settingContent}>
            <Text style={styles.settingTitle}>Alertas Geográficas</Text>
            <Text style={styles.settingSubtitle}>
              Recibe notificaciones de mascotas cerca de ti
            </Text>
          </View>
          <Ionicons name="chevron-forward" size={20} color="#999" />
        </TouchableOpacity>
        
        {/* Otros botones... */}
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F5F5F5',
  },
  section: {
    marginTop: 24,
    paddingHorizontal: 16,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#000',
    marginBottom: 12,
    marginLeft: 4,
  },
  settingItem: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#FFF',
    padding: 16,
    marginVertical: 4,
    borderRadius: 12,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 2,
    elevation: 2,
  },
  settingIcon: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: '#F0F9FF',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
  },
  settingContent: {
    flex: 1,
  },
  settingTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#000',
    marginBottom: 2,
  },
  settingSubtitle: {
    fontSize: 13,
    color: '#666',
  },
});
```

## Testing

Después de agregar el botón:

1. Recarga la app
2. Ve a la tab de Perfil
3. Deberías ver el nuevo botón "Alertas Geográficas"
4. Tócalo para abrir la pantalla de configuración
5. Verifica que la navegación funciona correctamente

---

**¡Listo! El botón está integrado y funcional.**

Elige la opción que mejor se adapte al diseño de tu app.

