import { create } from 'zustand';
import { authService, profileService } from '../services/supabase';

export const useAuthStore = create((set, get) => ({
  // Estado inicial
  user: null,
  session: null,
  loading: false,
  initialized: false,

  // Actions para actualizar estado
  setUser: (user) => set({ user }),
  setSession: (session) => set({ session }),
  setLoading: (loading) => set({ loading }),
  setInitialized: (initialized) => set({ initialized }),

  // Función de login
  login: async (email, password) => {
    try {
      set({ loading: true });
      
      const { data, error } = await authService.signIn(email, password);
      
      if (error) {
        set({ loading: false });
        return { success: false, error };
      }

      // Actualizar estado con datos del usuario y sesión
      set({
        user: data.user,
        session: data.session,
        loading: false,
      });

      // Asegurar que el perfil existe después del login
      if (data.user) {
        try {
          await profileService.ensureProfile(data.user.id, {
            full_name: data.user.user_metadata?.full_name || data.user.email?.split('@')[0] || 'Usuario',
          });
        } catch (profileError) {
          // No es crítico si falla, el perfil se creará en el próximo intento
          console.warn('No se pudo asegurar el perfil después del login:', profileError);
        }
      }

      return { success: true, data };
    } catch (error) {
      set({ loading: false });
      return { success: false, error };
    }
  },

  // Función de logout
  logout: async () => {
    try {
      set({ loading: true });
      
      const { error } = await authService.signOut();
      
      if (error) {
        set({ loading: false });
        return { success: false, error };
      }

      // Limpiar estado
      set({
        user: null,
        session: null,
        loading: false,
      });

      return { success: true };
    } catch (error) {
      set({ loading: false });
      return { success: false, error };
    }
  },

  // Función de registro
  signUp: async (email, password, fullName) => {
    try {
      set({ loading: true });
      
      const { data, error } = await authService.signUp(email, password, fullName);
      
      set({ loading: false });
      
      if (error) {
        return { success: false, error };
      }

      // En registro, no establecemos sesión inmediatamente
      // El usuario debe verificar su email primero
      return { success: true, data };
    } catch (error) {
      set({ loading: false });
      return { success: false, error };
    }
  },

  // Función de inicialización para verificar sesión existente
  initialize: async () => {
    try {
      set({ loading: true });
      
      const { session, error: sessionError } = await authService.getSession();
      
      if (sessionError) {
        set({ loading: false, initialized: true });
        return { success: false, error: sessionError };
      }

      if (session?.user) {
        const { user, error: userError } = await authService.getCurrentUser();
        
        if (userError) {
          set({ loading: false, initialized: true });
          return { success: false, error: userError };
        }

        set({
          user: user,
          session: session,
          loading: false,
          initialized: true,
        });

        // Asegurar que el perfil existe al inicializar
        if (user) {
          try {
            await profileService.ensureProfile(user.id, {
              full_name: user.user_metadata?.full_name || user.email?.split('@')[0] || 'Usuario',
            });
          } catch (profileError) {
            console.warn('No se pudo asegurar el perfil durante la inicialización:', profileError);
          }
        }
      } else {
        set({
          user: null,
          session: null,
          loading: false,
          initialized: true,
        });
      }

      return { success: true };
    } catch (error) {
      set({ loading: false, initialized: true });
      return { success: false, error };
    }
  },

  // Función para refrescar datos del usuario
  refreshUser: async () => {
    try {
      const { user, error } = await authService.getCurrentUser();
      
      if (error) {
        return { success: false, error };
      }

      set({ user });
      return { success: true, user };
    } catch (error) {
      return { success: false, error };
    }
  },

  // Función para actualizar perfil del usuario
  updateProfile: async (updates) => {
    try {
      const { user } = get();
      
      if (!user) {
        return { success: false, error: new Error('Usuario no autenticado') };
      }

      // Aquí podrías llamar a profileService.updateProfile si lo tienes
      // Por ahora solo actualizamos el estado local
      set({ user: { ...user, ...updates } });
      
      return { success: true };
    } catch (error) {
      return { success: false, error };
    }
  },

  // Función para verificar si el usuario está autenticado
  isAuthenticated: () => {
    const { user, session } = get();
    return !!(user && session);
  },

  // Función para obtener el ID del usuario
  getUserId: () => {
    const { user } = get();
    return user?.id || null;
  },

  // Función para limpiar el estado (útil para errores)
  clearAuth: () => {
    set({
      user: null,
      session: null,
      loading: false,
    });
  },

  // Suscribirse a cambios de autenticación
  subscribeToAuthChanges: () => {
    return authService.onAuthStateChange(async (event, session) => {
      console.log('🔐 Auth state changed:', event, session?.user?.email || 'sin usuario');
      
      if (event === 'SIGNED_IN' || event === 'TOKEN_REFRESHED') {
        // Obtener el usuario actualizado
        const { user, error } = await authService.getCurrentUser();
        
        if (!error && user) {
          set({
            user: user,
            session: session,
          });
          
          // Asegurar que el perfil existe
          try {
            await profileService.ensureProfile(user.id, {
              full_name: user.user_metadata?.full_name || user.email?.split('@')[0] || 'Usuario',
            });
          } catch (profileError) {
            console.warn('Error asegurando perfil:', profileError);
          }
        }
      } else if (event === 'SIGNED_OUT') {
        set({
          user: null,
          session: null,
        });
      } else if (event === 'USER_UPDATED') {
        const { user, error } = await authService.getCurrentUser();
        if (!error && user) {
          set({ user: user });
        }
      }
    });
  },

  // Función para recuperar contraseña
  resetPassword: async (email) => {
    try {
      set({ loading: true });
      const { data, error } = await authService.resetPassword(email);
      set({ loading: false });
      
      if (error) {
        return { success: false, error };
      }
      
      return { success: true, data };
    } catch (error) {
      set({ loading: false });
      return { success: false, error };
    }
  },

  // Función para actualizar contraseña
  updatePassword: async (newPassword) => {
    try {
      set({ loading: true });
      const { data, error } = await authService.updatePassword(newPassword);
      set({ loading: false });
      
      if (error) {
        return { success: false, error };
      }
      
      return { success: true, data };
    } catch (error) {
      set({ loading: false });
      return { success: false, error };
    }
  },

  // Función para reenviar confirmación de email
  resendConfirmation: async (email) => {
    try {
      set({ loading: true });
      const { data, error } = await authService.resendConfirmation(email);
      set({ loading: false });
      
      if (error) {
        return { success: false, error };
      }
      
      return { success: true, data };
    } catch (error) {
      set({ loading: false });
      return { success: false, error };
    }
  },
}));

