import { View, Text } from "react-native";
import { useLocalSearchParams } from "expo-router";

const PropertyDetailScreen = () => {
  const { id } = useLocalSearchParams<{ id: string }>();

  return (
    <View className="flex-1 items-center justify-center bg-white">
      <Text className="text-xl font-semibold text-gray-800">Property Detail</Text>
      <Text className="mt-2 text-gray-500">ID: {id}</Text>
    </View>
  );
};

export default PropertyDetailScreen;
