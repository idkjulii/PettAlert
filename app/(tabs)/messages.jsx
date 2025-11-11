import { useFocusEffect, useRouter } from 'expo-router';
import React, { useCallback } from 'react';
import { FlatList, RefreshControl, StyleSheet, View } from 'react-native';
import {
    ActivityIndicator,
    Avatar,
    Badge,
    Button,
    Card,
    List,
    Text,
    Title,
} from 'react-native-paper';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useConversations } from '../../src/hooks/useConversations';
import { useAuthStore } from '../../src/stores/authStore';

export default function MessagesScreen() {
  const router = useRouter();
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated());
  const { conversations, loading, error, refreshing, refresh, refetch } = useConversations();
  const getUserId = useAuthStore((state) => state.getUserId);
  const userId = getUserId();

  useFocusEffect(
    useCallback(() => {
      refetch({ showLoader: false });
    }, [refetch])
  );

  const handleConversationPress = useCallback(
    (conversationId) => {
      if (!conversationId) return;
      router.push({
        pathname: '/messages/[conversationId]',
        params: { conversationId },
      });
    },
    [router]
  );

  const renderAvatar = useCallback((conversation) => {
    if (conversation.other_user_avatar) {
      return (
        <Avatar.Image
          size={48}
          source={{ uri: conversation.other_user_avatar }}
          style={styles.avatar}
        />
      );
    }

    const label = (conversation.other_user_name || 'Usuario').slice(0, 2).toUpperCase();
    return <Avatar.Text size={48} label={label} style={styles.avatar} />;
  }, []);

  const formatTimestamp = useCallback((timestamp) => {
    if (!timestamp) return '';

    try {
      const date = new Date(timestamp);
      const now = new Date();
      const isToday =
        date.getDate() === now.getDate() &&
        date.getMonth() === now.getMonth() &&
        date.getFullYear() === now.getFullYear();

      if (isToday) {
        return date.toLocaleTimeString('es-ES', {
          hour: '2-digit',
          minute: '2-digit',
        });
      }

      return date.toLocaleDateString('es-ES', {
        day: '2-digit',
        month: 'short',
      });
    } catch {
      return '';
    }
  }, []);

  const renderConversation = ({ item }) => {
    const lastMessagePreview =
      item.last_message_content || item.last_message_image_url
        ? item.last_message_content || '📷 Foto'
        : 'Toca para comenzar a chatear';

    const timestamp = item.last_message_created_at || item.updated_at;
    const isOwnLastMessage = item.last_message_sender_id === userId;

    return (
      <List.Item
        style={styles.listItem}
        title={item.other_user_name || 'Usuario'}
        description={`${isOwnLastMessage ? 'Tú: ' : ''}${lastMessagePreview}`}
        onPress={() => handleConversationPress(item.conversation_id)}
        left={() => renderAvatar(item)}
        right={() => (
          <View style={styles.metaInfo}>
            <Text style={styles.timestamp}>{formatTimestamp(timestamp)}</Text>
            {item.unread_count > 0 && (
              <Badge style={styles.badge}>{item.unread_count}</Badge>
            )}
          </View>
        )}
      />
    );
  };

  if (loading) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.loadingContainer}>
          <ActivityIndicator size="large" color="#007AFF" />
          <Text style={styles.loadingText}>Cargando mensajes...</Text>
        </View>
      </SafeAreaView>
    );
  }

  if (!isAuthenticated) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.centerContent}>
          <Title style={styles.title}>Inicia sesión</Title>
          <Text style={styles.infoText}>
            Necesitas una cuenta para enviar y recibir mensajes sobre reportes.
          </Text>
          <Button
            mode="contained"
            style={styles.primaryButton}
            onPress={() => router.push('/(auth)/login')}
          >
            Iniciar sesión
          </Button>
        </View>
      </SafeAreaView>
    );
  }

  if (error) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.centerContent}>
          <Title style={styles.title}>Algo salió mal</Title>
          <Text style={styles.infoText}>{error}</Text>
          <Button mode="contained" onPress={refresh}>
            Reintentar
          </Button>
        </View>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <FlatList
        data={conversations}
        keyExtractor={(item) => item.conversation_id}
        renderItem={renderConversation}
        ItemSeparatorComponent={() => <View style={styles.separator} />}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={refresh} tintColor="#007AFF" />
        }
        contentContainerStyle={[styles.scrollContent, conversations.length === 0 && { flex: 1 }]}
        ListHeaderComponent={() => (
          <View style={styles.headerWrapper}>
            <Title style={styles.title}>Mensajes</Title>
            <Text style={styles.subtitle}>
              Chatea con otros usuarios para coordinar sobre mascotas perdidas o encontradas.
            </Text>
          </View>
        )}
        ListEmptyComponent={() => (
          <View style={styles.emptyState}>
            <Card style={styles.emptyCard}>
              <Card.Content style={styles.emptyContent}>
                <Text style={styles.emptyText}>No tienes conversaciones todavía</Text>
                <Text style={styles.emptySubtext}>
                  Busca un reporte y toca “Contactar” para iniciar un chat con el creador del reporte.
                </Text>
              </Card.Content>
            </Card>
          </View>
        )}
      />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  centerContent: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: 24,
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
  scrollContent: {
    paddingHorizontal: 12,
    paddingBottom: 24,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 20,
    textAlign: 'center',
  },
  subtitle: {
    fontSize: 14,
    color: '#666',
    marginBottom: 12,
    lineHeight: 20,
  },
  headerWrapper: {
    paddingHorizontal: 4,
    paddingTop: 16,
    paddingBottom: 12,
  },
  separator: {
    height: StyleSheet.hairlineWidth,
    backgroundColor: '#E0E0E0',
    marginLeft: 76,
  },
  listItem: {
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    marginHorizontal: 4,
    paddingVertical: 4,
  },
  avatar: {
    marginRight: 12,
    backgroundColor: '#E0E7FF',
  },
  metaInfo: {
    alignItems: 'flex-end',
    justifyContent: 'center',
    minWidth: 60,
  },
  timestamp: {
    fontSize: 12,
    color: '#999',
    marginBottom: 4,
  },
  badge: {
    backgroundColor: '#FF3B30',
  },
  emptyState: {
    flex: 1,
    justifyContent: 'center',
    paddingHorizontal: 16,
    paddingTop: 32,
  },
  emptyCard: {
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
    lineHeight: 20,
  },
  infoText: {
    fontSize: 14,
    color: '#666',
    lineHeight: 20,
  },
  primaryButton: {
    marginTop: 20,
  },
});

