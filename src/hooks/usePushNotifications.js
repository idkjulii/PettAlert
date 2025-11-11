import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { Platform } from 'react-native';
import * as Notifications from 'expo-notifications';
import Constants from 'expo-constants';
import { notificationService } from '../services/supabase';
import { useAuthStore } from '../stores/authStore';

Notifications.setNotificationHandler({
  handleNotification: async () => ({
    shouldShowAlert: true,
    shouldPlaySound: false,
    shouldSetBadge: false,
  }),
});

const getProjectId = () => {
  const expoConfig = Constants.expoConfig ?? Constants.manifest;
  const candidate =
    expoConfig?.extra?.eas?.projectId ??
    Constants.easConfig?.projectId ??
    process.env.EXPO_PUBLIC_EAS_PROJECT_ID ??
    null;

  const uuidRegex =
    /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;

  if (candidate && uuidRegex.test(String(candidate))) {
    return candidate;
  }

  console.warn(
    '[usePushNotifications] projectId no válido o no disponible. Se usará getExpoPushTokenAsync sin projectId.'
  );
  return null;
};

export const usePushNotifications = () => {
  const userId = useAuthStore((state) => state.user?.id || null);
  const [expoToken, setExpoToken] = useState(null);
  const [status, setStatus] = useState(null);
  const [error, setError] = useState(null);
  const [registering, setRegistering] = useState(false);
  const notificationListener = useRef(null);
  const responseListener = useRef(null);

  const ensureAndroidChannel = useCallback(async () => {
    if (Platform.OS !== 'android') {
      return;
    }

    await Notifications.setNotificationChannelAsync('default', {
      name: 'Mensajes',
      importance: Notifications.AndroidImportance.MAX,
      vibrationPattern: [0, 250, 250, 250],
      lightColor: '#FF231F7C',
      bypassDnd: false,
      sound: 'default',
      lockscreenVisibility: Notifications.AndroidNotificationVisibility.PUBLIC,
    });
  }, []);

  const registerPushToken = useCallback(async () => {
    if (!userId || registering) {
      return;
    }

    setRegistering(true);
    setError(null);

    try {
      await ensureAndroidChannel();

      const projectId = getProjectId();
      if (!projectId) {
        console.warn(
          '[usePushNotifications] No se encontró un projectId válido. Configura EXPO_PUBLIC_EAS_PROJECT_ID o eas.projectId en app.config.js.'
        );
        setError(
          'Las notificaciones push requieren configurar un Project ID de Expo (EAS). Revisa app.config.js o EXPO_PUBLIC_EAS_PROJECT_ID.'
        );
        return;
      }

      const { status: existingStatus } = await Notifications.getPermissionsAsync();
      let finalStatus = existingStatus;

      if (existingStatus !== 'granted') {
        const { status: requestedStatus } = await Notifications.requestPermissionsAsync();
        finalStatus = requestedStatus;
      }

      setStatus(finalStatus);

      if (finalStatus !== 'granted') {
        throw new Error('Los permisos de notificaciones fueron denegados.');
      }

      let tokenResponse;

      try {
        tokenResponse = await Notifications.getExpoPushTokenAsync({ projectId });
      } catch (err) {
        console.warn(
          '[usePushNotifications] Falló getExpoPushTokenAsync con projectId.',
          err?.message || err
        );
        throw err;
      }
      const token = tokenResponse.data;

      setExpoToken(token);

      await notificationService.registerToken({
        userId,
        expoPushToken: token,
        platform: Platform.OS,
      });
    } catch (err) {
      console.error('Error registrando notificaciones push:', err);
      setError(err?.message || 'Error registrando notificaciones push.');
    } finally {
      setRegistering(false);
    }
  }, [ensureAndroidChannel, registering, userId]);

  useEffect(() => {
    if (!userId) {
      setExpoToken(null);
      setStatus(null);
      setError(null);
      return;
    }

    registerPushToken();
  }, [registerPushToken, userId]);

  useEffect(() => {
    notificationListener.current = Notifications.addNotificationReceivedListener(() => {
      // Podríamos manejar métricas o actualizar estado aquí si fuese necesario.
    });

    responseListener.current = Notifications.addNotificationResponseReceivedListener(() => {
      // Idealmente manejar la navegación hacia la conversación cuando se abre la notificación.
    });

    return () => {
      if (notificationListener.current) {
        try {
          notificationListener.current.remove?.();
        } catch {
          Notifications.removeNotificationSubscription?.(notificationListener.current);
        } finally {
          notificationListener.current = null;
        }
      }
      if (responseListener.current) {
        try {
          responseListener.current.remove?.();
        } catch {
          Notifications.removeNotificationSubscription?.(responseListener.current);
        } finally {
          responseListener.current = null;
        }
      }
    };
  }, []);

  const summary = useMemo(
    () => ({
      expoToken,
      status,
      error,
      registering,
      refresh: registerPushToken,
    }),
    [error, expoToken, registering, registerPushToken, status]
  );

  return summary;
};


