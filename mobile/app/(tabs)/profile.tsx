import { Pressable, Text, View } from "react-native";
import { useRouter } from "expo-router";

import useAuthStore from "@/stores/authStore";

const ProfileScreen = () => {
  const router = useRouter();
  const logout = useAuthStore((state) => state.logout);
  const user = useAuthStore((state) => state.user);

  const handleLogout = async () => {
    await logout();
    router.replace("/(auth)/login");
  };

  return (
    <View className="flex-1 items-center justify-center gap-3 bg-white px-6">
      <Text className="text-xl font-semibold text-gray-800">Profile</Text>
      <Text className="text-gray-500">{user?.email ?? "Manage your account"}</Text>

      <Pressable className="mt-3 rounded-xl bg-gray-900 px-5 py-3" onPress={handleLogout}>
        <Text className="font-semibold text-white">Logout</Text>
      </Pressable>
    </View>
  );
};

export default ProfileScreen;
