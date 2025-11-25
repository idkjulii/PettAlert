import { Stack } from 'expo-router';

export default function PetsLayout() {
  return (
    <Stack
      screenOptions={{
        headerStyle: {
          backgroundColor: '#007AFF',
        },
        headerTintColor: '#fff',
        headerTitleStyle: {
          fontWeight: 'bold',
        },
      }}
    >
      <Stack.Screen
        name="[petId]"
        options={{
          title: 'Detalle de Mascota',
        }}
      />
      <Stack.Screen
        name="create"
        options={{
          title: 'Registrar Mascota',
        }}
      />
      <Stack.Screen
        name="[petId]/add-health-event"
        options={{
          title: 'Agregar Evento de Salud',
        }}
      />
      <Stack.Screen
        name="[petId]/add-vaccination"
        options={{
          title: 'Agregar Vacunación',
        }}
      />
      <Stack.Screen
        name="[petId]/add-medication"
        options={{
          title: 'Agregar Medicamento',
        }}
      />
      <Stack.Screen
        name="[petId]/add-wellness"
        options={{
          title: 'Registrar Indicador',
        }}
      />
      <Stack.Screen
        name="[petId]/add-reminder"
        options={{
          title: 'Crear Recordatorio',
        }}
      />
    </Stack>
  );
}

