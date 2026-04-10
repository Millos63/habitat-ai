import { View, Text } from "react-native";

const FavoritesScreen = () => {
  return (
    <View className="flex-1 items-center justify-center bg-white">
      <Text className="text-xl font-semibold text-gray-800">Favorites</Text>
      <Text className="mt-2 text-gray-500">Your saved properties</Text>
    </View>
  );
};

export default FavoritesScreen;
