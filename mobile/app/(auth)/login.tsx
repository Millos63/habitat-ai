import { View, Text } from "react-native";

const LoginScreen = () => {
  return (
    <View className="flex-1 items-center justify-center bg-white">
      <Text className="text-2xl font-bold text-primary-500">Welcome Back</Text>
      <Text className="mt-2 text-gray-500">Sign in to your account</Text>
    </View>
  );
};

export default LoginScreen;
