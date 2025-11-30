/**
 * Pantalla de configuración de alertas geográficas
 * Accesible desde el perfil del usuario
 */

import React from 'react';
import { View, StyleSheet, SafeAreaView, Platform, StatusBar } from 'react-native';
import { Stack, useRouter } from 'expo-router';
import { GeoAlertsSettings } from '../components/GeoAlerts/GeoAlertsSettings';

export default function GeoAlertsSettingsScreen() {
  const router = useRouter();

  return (
    <SafeAreaView style={styles.container}>
      <Stack.Screen
        options={{
          title: 'Alertas Geográficas',
          headerShown: true,
          presentation: 'modal',
          headerLeft: () => null,
        }}
      />
      <GeoAlertsSettings onClose={() => router.back()} />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F5F5F5',
    paddingTop: Platform.OS === 'android' ? StatusBar.currentHeight : 0,
  },
});


