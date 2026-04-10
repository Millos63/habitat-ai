import { View, Text } from "react-native";

const DashboardScreen = () => {
  return (
    <View className="flex-1 items-center justify-center bg-white">
      <Text className="text-2xl font-bold text-primary-500">Agent Dashboard</Text>
      <Text className="mt-2 text-gray-500">Manage your listings</Text>
    </View>
  );
};

export default DashboardScreen;
