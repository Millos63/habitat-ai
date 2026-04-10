import { Stack } from "expo-router";

const AgentLayout = () => {
  return (
    <Stack screenOptions={{ headerShown: true }}>
      <Stack.Screen name="dashboard" options={{ title: "Dashboard" }} />
    </Stack>
  );
};

export default AgentLayout;
