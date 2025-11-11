import { useCallback, useEffect, useRef, useState } from 'react';
import { messageService } from '../services/supabase';
import { useAuthStore } from '../stores/authStore';
import { eventBus } from '../utils/eventBus';

export const useConversations = () => {
  const getUserId = useAuthStore((state) => state.getUserId);
  const [conversations, setConversations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState(null);
  const subscriptionRef = useRef(null);

  const clearedConversationsRef = useRef(new Set());

  const fetchConversations = useCallback(
    async ({ showLoader = true } = {}) => {
      const userId = getUserId();

      if (!userId) {
        setConversations([]);
        setLoading(false);
        return;
      }

      if (showLoader) {
        setLoading(true);
      }

      setError(null);

      try {
        const { data, error: fetchError } = await messageService.getUserConversations(userId);

        if (fetchError) {
          throw fetchError;
        }

        const processed =
          data?.map((conversation) => {
            if (clearedConversationsRef.current.has(conversation.conversation_id)) {
              return { ...conversation, unread_count: 0 };
            }
            return conversation;
          }) || [];

        setConversations(processed);
      } catch (err) {
        console.error('Error cargando conversaciones:', err);
        setError(err?.message || 'No se pudieron cargar las conversaciones.');
      } finally {
        if (showLoader) {
          setLoading(false);
        }
      }
    },
    [getUserId]
  );

  const refresh = useCallback(async () => {
    setRefreshing(true);
    await fetchConversations({ showLoader: false });
    setRefreshing(false);
  }, [fetchConversations]);

  useEffect(() => {
    fetchConversations();

    const userId = getUserId();

    if (subscriptionRef.current) {
      messageService.removeChannel(subscriptionRef.current);
    }

    if (!userId) {
      return undefined;
    }

    subscriptionRef.current = messageService.subscribeToConversations(userId, () => {
      fetchConversations({ showLoader: false });
    });

    return () => {
      if (subscriptionRef.current) {
        messageService.removeChannel(subscriptionRef.current);
        subscriptionRef.current = null;
      }
    };
  }, [fetchConversations, getUserId]);

  useEffect(() => {
    const offRead = eventBus.on('conversation:read', (conversationId) => {
      if (!conversationId) return;
      clearedConversationsRef.current.add(conversationId);
      setConversations((prev) =>
        prev.map((conversation) =>
          conversation.conversation_id === conversationId
            ? { ...conversation, unread_count: 0 }
            : conversation
        )
      );
    });

    return () => {
      offRead();
    };
  }, [getUserId]);

  return {
    conversations,
    loading,
    error,
    refreshing,
    refresh,
    refetch: fetchConversations,
  };
};


