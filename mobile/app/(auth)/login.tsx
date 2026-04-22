import { useState } from "react";
import { isAxiosError } from "axios";
import {
  ActivityIndicator,
  Alert,
  KeyboardAvoidingView,
  Platform,
  Pressable,
  Text,
  TextInput,
  View,
} from "react-native";
import { Link, useRouter } from "expo-router";

import authService from "@/services/auth.service";
import useAuthStore from "@/stores/authStore";

const getApiErrorMessage = (error: unknown, fallback: string): string => {
  if (!isAxiosError(error)) {
    return fallback;
  }

  const detail = error.response?.data?.detail;
  if (typeof detail === "string") {
    return detail;
  }

  if (Array.isArray(detail) && detail.length > 0) {
    const first = detail[0] as { msg?: string };
    if (first?.msg) {
      return first.msg;
    }
  }

  return fallback;
};

const LoginScreen = () => {
  const router = useRouter();
  const setAuth = useAuthStore((state) => state.setAuth);
  const setUser = useAuthStore((state) => state.setUser);

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleLogin = async () => {
    const normalizedEmail = email.trim().toLowerCase();

    if (!normalizedEmail || !password.trim()) {
      Alert.alert("Missing fields", "Please enter email and password.");
      return;
    }

    const emailIsValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(normalizedEmail);
    if (!emailIsValid) {
      Alert.alert("Invalid email", "Please enter a valid email address.");
      return;
    }

    try {
      setIsSubmitting(true);
      const auth = await authService.login({
        email: normalizedEmail,
        password,
      });

      await setAuth(auth.access_token);
      const me = await authService.getMe();
      setUser(me);

      router.replace("/(tabs)");
    } catch (error) {
      const message = getApiErrorMessage(error, "Invalid credentials or backend unavailable.");
      Alert.alert("Login failed", message);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <KeyboardAvoidingView
      className="flex-1 bg-white"
      behavior={Platform.OS === "ios" ? "padding" : undefined}
    >
      <View className="flex-1 justify-center px-6">
        <Text className="text-3xl font-bold text-primary-500">Welcome Back</Text>
        <Text className="mt-2 text-gray-500">Sign in to your account</Text>

        <View className="mt-8 gap-4">
          <View>
            <Text className="mb-2 text-sm font-medium text-gray-700">Email</Text>
            <TextInput
              className="rounded-xl border border-gray-300 px-4 py-3"
              placeholder="you@example.com"
              placeholderTextColor="#9CA3AF"
              autoCapitalize="none"
              keyboardType="email-address"
              value={email}
              onChangeText={setEmail}
            />
          </View>

          <View>
            <Text className="mb-2 text-sm font-medium text-gray-700">Password</Text>
            <TextInput
              className="rounded-xl border border-gray-300 px-4 py-3"
              placeholder="••••••••"
              placeholderTextColor="#9CA3AF"
              secureTextEntry
              value={password}
              onChangeText={setPassword}
            />
          </View>

          <Pressable
            className="mt-2 items-center rounded-xl bg-primary-500 py-3"
            onPress={handleLogin}
            disabled={isSubmitting}
          >
            {isSubmitting ? (
              <ActivityIndicator color="#fff" />
            ) : (
              <Text className="font-semibold text-white">Sign In</Text>
            )}
          </Pressable>

          <View className="flex-row justify-center">
            <Text className="text-gray-500">Don&apos;t have an account? </Text>
            <Link href="/(auth)/register" asChild>
              <Pressable>
                <Text className="font-semibold text-primary-500">Register</Text>
              </Pressable>
            </Link>
          </View>
        </View>
      </View>
    </KeyboardAvoidingView>
  );
};

export default LoginScreen;
