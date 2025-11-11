import { Stack } from 'expo-router';

export default function MessagesLayout() {
  return (
    <Stack>
      <Stack.Screen
        name="[conversationId]"
        options={{
          title: 'Conversación',
          headerShown: false,
        }}
      />
    </Stack>
  );
}


