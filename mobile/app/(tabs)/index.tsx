import { View, Text } from "react-native";

const HomeScreen = () => {
  return (
    <View className="flex-1 items-center justify-center bg-white">
      <Text className="text-2xl font-bold text-primary-500">Habitat AI</Text>
      <Text className="mt-2 text-gray-500">Find your dream property</Text>
    </View>
  );
};

export default HomeScreen;
