import React, { useEffect, useRef, useState } from 'react';
import { ActivityIndicator, Alert, StyleSheet, View } from 'react-native';
import MapView, { Circle, Marker, PROVIDER_DEFAULT } from 'react-native-maps';
import { getCurrentLocation } from '../../services/location';
import ReportMarker from './ReportMarker';

const CustomMapView = ({ 
  reports = [],
  onReportPress,
  onLocationSelect,
  showUserLocation = true,
  showRadius = false,
  radiusMeters = 5000,
  initialRegion = null,
  style,
  allowLocationSelection = false,
  selectedLocation = null,
}) => {
  const mapRef = useRef(null);
  const [userLocation, setUserLocation] = useState(null);
  const [loading, setLoading] = useState(true);
  const [region, setRegion] = useState(initialRegion);

  useEffect(() => {
    getUserLocation();
  }, []);

  const getUserLocation = async () => {
    try {
      const location = await getCurrentLocation();
      
      if (location.error || !location.latitude || !location.longitude) {
        Alert.alert(
          'Error de ubicación',
          'No se pudo obtener tu ubicación. Por favor, verifica los permisos.',
        );
        setLoading(false);
        return;
      }

      setUserLocation({
        latitude: location.latitude,
        longitude: location.longitude,
      });

      if (!region) {
        setRegion({
          latitude: location.latitude,
          longitude: location.longitude,
          latitudeDelta: 0.05,
          longitudeDelta: 0.05,
        });
      }

      setLoading(false);
    } catch (error) {
      console.error('Error obteniendo ubicación:', error);
      setLoading(false);
    }
  };

  const handleMapPress = (event) => {
    if (allowLocationSelection && onLocationSelect) {
      const { latitude, longitude } = event.nativeEvent.coordinate;
      onLocationSelect({ latitude, longitude });
    }
  };

  if (loading) {
    return (
      <View style={[styles.container, styles.loadingContainer]}>
        <ActivityIndicator size="large" color="#007AFF" />
      </View>
    );
  }

  return (
    <View style={[styles.container, style]}>
      <MapView
        ref={mapRef}
        style={styles.map}
        provider={PROVIDER_DEFAULT}
        initialRegion={region}
        showsUserLocation={showUserLocation}
        showsMyLocationButton={false}
        showsCompass={true}
        showsScale={true}
        loadingEnabled={true}
        onRegionChangeComplete={setRegion}
        onPress={handleMapPress}
      >
        {showRadius && userLocation && (
          <Circle
            center={userLocation}
            radius={radiusMeters}
            strokeColor="rgba(0, 122, 255, 0.3)"
            fillColor="rgba(0, 122, 255, 0.1)"
            strokeWidth={2}
          />
        )}

        {reports.map((report) => {
          let latitude, longitude;
          
          // Intentar obtener coordenadas de diferentes formatos
          if (report.latitude && report.longitude) {
            // Coordenadas directas
            latitude = report.latitude;
            longitude = report.longitude;
          } else if (report.location?.coordinates) {
            // Formato GeoJSON: [longitude, latitude]
            longitude = report.location.coordinates[0];
            latitude = report.location.coordinates[1];
          } else if (typeof report.location === 'string' && report.location.includes('POINT')) {
            // Formato PostGIS POINT: "POINT(longitude latitude)"
            const match = report.location.match(/POINT\(([^)]+)\)/);
            if (match) {
              const [lng, lat] = match[1].split(' ').map(Number);
              longitude = lng;
              latitude = lat;
            }
          }

          if (!latitude || !longitude) {
            // Debug: mostrar qué reporte no tiene coordenadas válidas
            console.log('⚠️ Reporte sin coordenadas válidas:', {
              id: report.id,
              type: report.type,
              location: report.location,
              latitude: report.latitude,
              longitude: report.longitude
            });
            return null;
          }

          // Debug: mostrar reporte que se va a renderizar
          console.log('🗺️ Renderizando marcador para reporte:', {
            id: report.id,
            type: report.type,
            coordinates: { latitude, longitude }
          });

          return (
            <ReportMarker
              key={report.id}
              report={report}
              coordinate={{ latitude, longitude }}
              onPress={() => onReportPress && onReportPress(report)}
            />
          );
        })}

        {allowLocationSelection && selectedLocation && (
          <Marker
            coordinate={selectedLocation}
            pinColor="#007AFF"
            title="Ubicación seleccionada"
          />
        )}
      </MapView>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  loadingContainer: {
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#f5f5f5',
  },
  map: {
    width: '100%',
    height: '100%',
  },
});

export default CustomMapView;

