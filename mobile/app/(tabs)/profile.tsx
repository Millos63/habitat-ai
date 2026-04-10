import { View, Text } from "react-native";

const ProfileScreen = () => {
  return (
    <View className="flex-1 items-center justify-center bg-white">
      <Text className="text-xl font-semibold text-gray-800">Profile</Text>
      <Text className="mt-2 text-gray-500">Manage your account</Text>
    </View>
  );
};

export default ProfileScreen;
