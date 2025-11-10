import { useRouter } from 'expo-router';
import React, { useEffect, useState } from 'react';
import { Alert, Image, ScrollView, StyleSheet, View } from 'react-native';
import { ActivityIndicator, Button, Card, IconButton, Text, Title } from 'react-native-paper';
import { SafeAreaView } from 'react-native-safe-area-context';
import { reportService } from '../../src/services/supabase';
import { useAuthStore } from '../../src/stores/authStore';
import { useMatchesStore } from '../../src/stores/matchStore';

export default function ReportsScreen() {
  const { getUserId } = useAuthStore();
  const router = useRouter();
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [deletingId, setDeletingId] = useState(null);
  const [matchesLoadingId, setMatchesLoadingId] = useState(null);
  const matchesByReport = useMatchesStore((state) => state.matchesByReport);
  const setMatchesForReport = useMatchesStore((state) => state.setMatchesForReport);
  const clearMatchesForReport = useMatchesStore((state) => state.clearMatchesForReport);
  const [matchErrors, setMatchErrors] = useState({});

  useEffect(() => {
    loadUserReports();
  }, []);

  const loadUserReports = async () => {
    try {
      const userId = getUserId();
      if (!userId) {
        setLoading(false);
        return;
      }

      const { data, error } = await reportService.getUserReports(userId);
      
      if (error) {
        console.error('Error cargando reportes:', error);
      } else {
        // Filtrar reportes eliminados/cancelados
        const activeReports = (data || []).filter(report => report.status !== 'cancelled');
        setReports(activeReports);
      }
    } catch (error) {
      console.error('Error inesperado:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleEditReport = (report) => {
    if (report.type === 'lost') {
      router.push({
        pathname: '/report/create-lost',
        params: { reportId: report.id, editMode: 'true' }
      });
    } else {
      router.push({
        pathname: '/report/create-found',
        params: { reportId: report.id, editMode: 'true' }
      });
    }
  };

  const handleDeleteReport = (report) => {
    Alert.alert(
      'Eliminar reporte',
      `¿Estás seguro de que deseas eliminar este reporte de ${report.pet_name || 'tu mascota'}?`,
      [
        {
          text: 'Cancelar',
          style: 'cancel'
        },
        {
          text: 'Eliminar',
          style: 'destructive',
          onPress: async () => {
            try {
              setDeletingId(report.id);
              const { error } = await reportService.deleteReport(report.id);
              
              if (error) {
                Alert.alert('Error', 'No se pudo eliminar el reporte. Por favor, intenta de nuevo.');
                console.error('Error eliminando reporte:', error);
              } else {
                // Recargar la lista de reportes
                await loadUserReports();
                clearMatchesForReport(report.id);
                Alert.alert('Éxito', 'El reporte ha sido eliminado.');
              }
            } catch (error) {
              console.error('Error inesperado:', error);
              Alert.alert('Error', 'Ocurrió un error inesperado.');
            } finally {
              setDeletingId(null);
            }
          }
        }
      ]
    );
  };

  const handleViewMatchReport = (matchedReportId) => {
    if (!matchedReportId) return;
    router.push({
      pathname: '/report/[id]',
      params: { id: matchedReportId, from: 'reports' }
    });
  };

  const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

  const handleFindMatches = async (report) => {
    setMatchesLoadingId(report.id);
    setMatchErrors((prev) => ({ ...prev, [report.id]: null }));
    setMatchesForReport(report.id, null);

    try {
      // Disparar reprocesamiento en n8n (en segundo plano)
      const triggerResult = await reportService.requestMatchesAnalysis(report.id);
      if (triggerResult?.error) {
        console.warn('Error enviando reporte a n8n:', triggerResult.error);
      }

      // Intentar obtener coincidencias (polling corto)
      let matchesData = null;
      const maxAttempts = 4;
      for (let attempt = 0; attempt < maxAttempts; attempt++) {
        const { data, error } = await reportService.getMatchesForReport(report.id);
        if (error) {
          throw error;
        }

        matchesData = data;
        const hasMatches = data?.matches && data.matches.length > 0;
        if (hasMatches) {
          break;
        }

        if (attempt < maxAttempts - 1) {
          await sleep(1500);
        }
      }

      setMatchesForReport(report.id, matchesData);

      if (!matchesData?.matches?.length) {
        setMatchErrors((prev) => ({
          ...prev,
          [report.id]: 'No encontramos coincidencias todavía. Vuelve a intentarlo en unos minutos.'
        }));
      }
    } catch (error) {
      console.error('Error buscando coincidencias:', error);
      setMatchErrors((prev) => ({
        ...prev,
        [report.id]: error?.message || 'Ocurrió un error al buscar coincidencias.'
      }));
    } finally {
      setMatchesLoadingId(null);
    }
  };

  const renderMatches = (report) => {
    const matchesData = matchesByReport[report.id];
    const errorMessage = matchErrors[report.id];

    if (matchesLoadingId === report.id) {
      return (
        <View style={styles.matchLoadingContainer}>
          <ActivityIndicator size="small" color="#007AFF" />
          <Text style={styles.matchLoadingText}>Buscando coincidencias...</Text>
        </View>
      );
    }

    if (errorMessage) {
      return <Text style={styles.matchErrorText}>{errorMessage}</Text>;
    }

    if (!matchesData) {
      return null;
    }

    if (!matchesData.matches || matchesData.matches.length === 0) {
      return <Text style={styles.noMatchesText}>Sin coincidencias por ahora.</Text>;
    }

    return (
      <View style={styles.matchesContainer}>
        <Text style={styles.matchesTitle}>Coincidencias encontradas</Text>
        {matchesData.matches.map((match) => {
          const relatedReport =
            report.type === 'lost' ? match.found_report : match.lost_report;

          if (!relatedReport) {
            return null;
          }

          const rawSimilarity = typeof match.similarity_score === 'number' ? match.similarity_score : 0;
          const normalizedSimilarity = Math.max(0, Math.min(rawSimilarity, 1));
          const similarity = Math.round(normalizedSimilarity * 100);
          const photo =
            Array.isArray(relatedReport.photos) && relatedReport.photos.length > 0
              ? relatedReport.photos[0]
              : null;

          return (
            <Card key={match.match_id || `${report.id}-${relatedReport.id}`} style={styles.matchCard}>
              <View style={styles.matchRow}>
                {photo ? (
                  <Image source={{ uri: photo }} style={styles.matchImage} />
                ) : (
                  <View style={styles.matchImagePlaceholder}>
                    <Text style={styles.matchPlaceholderText}>Sin foto</Text>
                  </View>
                )}
                <View style={styles.matchInfo}>
                  <Text style={styles.matchScore}>Similitud: {similarity}%</Text>
                  <Text style={styles.matchDescription}>
                    {relatedReport.type === 'lost' ? 'Reporte de mascota perdida' : 'Reporte de mascota encontrada'}
                  </Text>
                  {relatedReport.pet_name ? (
                    <Text style={styles.matchPetName}>{relatedReport.pet_name}</Text>
                  ) : null}
                  <Button
                    mode="outlined"
                  onPress={() => handleViewMatchReport(relatedReport.id)}
                    style={styles.matchActionButton}
                  >
                    Ver reporte
                  </Button>
                </View>
              </View>
            </Card>
          );
        })}
      </View>
    );
  };

  if (loading) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.loadingContainer}>
          <ActivityIndicator size="large" color="#007AFF" />
          <Text style={styles.loadingText}>Cargando reportes...</Text>
        </View>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView style={styles.scrollView} contentContainerStyle={styles.scrollContent}>
        <Title style={styles.title}>Mis Reportes</Title>
        
        {reports.length === 0 ? (
          <Card style={styles.emptyCard}>
            <Card.Content style={styles.emptyContent}>
              <Text style={styles.emptyText}>
                📝 No tienes reportes creados aún
              </Text>
              <Text style={styles.emptySubtext}>
                Crea tu primer reporte desde la pantalla de inicio
              </Text>
            </Card.Content>
          </Card>
        ) : (
          reports.map((report) => (
            <Card key={report.id} style={styles.reportCard}>
              <Card.Content>
                <View style={styles.reportHeader}>
                  <View style={styles.reportHeaderLeft}>
                    <Text style={styles.reportType}>
                      {report.type === 'lost' ? '🔴 Mascota Perdida' : '🟢 Mascota Encontrada'}
                    </Text>
                  </View>
                  <View style={styles.reportActions}>
                    <IconButton
                      icon="pencil"
                      size={20}
                      iconColor="#007AFF"
                      onPress={() => handleEditReport(report)}
                      style={styles.actionButton}
                    />
                    <IconButton
                      icon="delete"
                      size={20}
                      iconColor="#FF3B30"
                      onPress={() => handleDeleteReport(report)}
                      style={styles.actionButton}
                      disabled={deletingId === report.id}
                    />
                  </View>
                </View>
                <Text style={styles.reportPetName}>
                  {report.pet_name || 'Sin nombre'}
                </Text>
                <Text style={styles.reportDescription} numberOfLines={2}>
                  {report.description || 'Sin descripción'}
                </Text>
                <Text style={styles.reportDate}>
                  📅 {new Date(report.created_at).toLocaleDateString()}
                </Text>
                <Text style={styles.reportStatus}>
                  Estado: {report.status === 'active' ? 'Activo' : 'Resuelto'}
                </Text>
                <Button
                  mode="contained"
                  onPress={() => handleFindMatches(report)}
                  style={styles.matchButton}
                  loading={matchesLoadingId === report.id}
                  disabled={matchesLoadingId === report.id}
                >
                  Buscar coincidencias
                </Button>
                {renderMatches(report)}
              </Card.Content>
            </Card>
          ))
        )}
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  loadingText: {
    marginTop: 16,
    fontSize: 16,
    color: '#666',
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
  emptyCard: {
    marginTop: 40,
    elevation: 2,
  },
  emptyContent: {
    alignItems: 'center',
    paddingVertical: 40,
  },
  emptyText: {
    fontSize: 18,
    color: '#666',
    textAlign: 'center',
    marginBottom: 8,
  },
  emptySubtext: {
    fontSize: 14,
    color: '#999',
    textAlign: 'center',
  },
  reportCard: {
    marginBottom: 16,
    elevation: 2,
  },
  reportHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  reportHeaderLeft: {
    flex: 1,
  },
  reportActions: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  actionButton: {
    margin: 0,
  },
  reportType: {
    fontSize: 16,
    fontWeight: 'bold',
  },
  reportPetName: {
    fontSize: 18,
    fontWeight: '600',
    color: '#333',
    marginBottom: 8,
  },
  reportDescription: {
    fontSize: 14,
    color: '#666',
    marginBottom: 8,
    lineHeight: 20,
  },
  reportDate: {
    fontSize: 12,
    color: '#999',
    marginBottom: 4,
  },
  reportStatus: {
    fontSize: 12,
    color: '#007AFF',
    fontWeight: '500',
  },
  matchButton: {
    marginTop: 12,
  },
  matchLoadingContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginTop: 12,
  },
  matchLoadingText: {
    marginLeft: 8,
    color: '#666',
  },
  matchesContainer: {
    marginTop: 12,
    backgroundColor: '#F3F7FF',
    borderRadius: 8,
    padding: 12,
  },
  matchesTitle: {
    fontWeight: '600',
    marginBottom: 8,
    color: '#1A4D8F',
  },
  matchCard: {
    marginBottom: 10,
    elevation: 1,
  },
  matchRow: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 10,
  },
  matchImage: {
    width: 70,
    height: 70,
    borderRadius: 8,
    marginRight: 12,
  },
  matchImagePlaceholder: {
    width: 70,
    height: 70,
    borderRadius: 8,
    marginRight: 12,
    backgroundColor: '#e0e0e0',
    justifyContent: 'center',
    alignItems: 'center',
  },
  matchPlaceholderText: {
    color: '#777',
    fontSize: 12,
  },
  matchInfo: {
    flex: 1,
  },
  matchScore: {
    fontWeight: 'bold',
    color: '#007AFF',
    marginBottom: 4,
  },
  matchDescription: {
    color: '#333',
    marginBottom: 4,
  },
  matchPetName: {
    fontStyle: 'italic',
    marginBottom: 6,
  },
  matchActionButton: {
    alignSelf: 'flex-start',
  },
  noMatchesText: {
    marginTop: 12,
    color: '#666',
    fontStyle: 'italic',
  },
  matchErrorText: {
    marginTop: 12,
    color: '#D32F2F',
    fontStyle: 'italic',
  },
});

