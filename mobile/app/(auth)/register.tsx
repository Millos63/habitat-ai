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

const RegisterScreen = () => {
  const router = useRouter();
  const setAuth = useAuthStore((state) => state.setAuth);
  const setUser = useAuthStore((state) => state.setUser);

  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleRegister = async () => {
    const normalizedName = fullName.trim();
    const normalizedEmail = email.trim().toLowerCase();

    if (!normalizedName || !normalizedEmail || !password.trim()) {
      Alert.alert("Missing fields", "Please complete all fields.");
      return;
    }

    if (normalizedName.length < 2) {
      Alert.alert("Invalid name", "Full name must be at least 2 characters.");
      return;
    }

    const emailIsValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(normalizedEmail);
    if (!emailIsValid) {
      Alert.alert("Invalid email", "Please enter a valid email address.");
      return;
    }

    if (password.length < 8) {
      Alert.alert("Weak password", "Password must be at least 8 characters.");
      return;
    }

    if (!/[A-Z]/.test(password) || !/[a-z]/.test(password) || !/\d/.test(password)) {
      Alert.alert(
        "Weak password",
        "Password must include uppercase, lowercase and at least one number.",
      );
      return;
    }

    try {
      setIsSubmitting(true);
      const auth = await authService.register({
        full_name: normalizedName,
        email: normalizedEmail,
        password,
      });

      await setAuth(auth.access_token);
      const me = await authService.getMe();
      setUser(me);

      router.replace("/(tabs)");
    } catch (error) {
      const message = getApiErrorMessage(error, "Could not create account.");
      Alert.alert("Register failed", message);
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
        <Text className="text-3xl font-bold text-primary-500">Create Account</Text>
        <Text className="mt-2 text-gray-500">Join Habitat AI</Text>

        <View className="mt-8 gap-4">
          <View>
            <Text className="mb-2 text-sm font-medium text-gray-700">Full name</Text>
            <TextInput
              className="rounded-xl border border-gray-300 px-4 py-3"
              placeholder="Your full name"
              placeholderTextColor="#9CA3AF"
              value={fullName}
              onChangeText={setFullName}
            />
          </View>

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
              placeholder="At least 8 characters"
              placeholderTextColor="#9CA3AF"
              secureTextEntry
              value={password}
              onChangeText={setPassword}
            />
          </View>

          <Pressable
            className="mt-2 items-center rounded-xl bg-primary-500 py-3"
            onPress={handleRegister}
            disabled={isSubmitting}
          >
            {isSubmitting ? (
              <ActivityIndicator color="#fff" />
            ) : (
              <Text className="font-semibold text-white">Create account</Text>
            )}
          </Pressable>

          <View className="flex-row justify-center">
            <Text className="text-gray-500">Already have an account? </Text>
            <Link href="/(auth)/login" asChild>
              <Pressable>
                <Text className="font-semibold text-primary-500">Sign In</Text>
              </Pressable>
            </Link>
          </View>
        </View>
      </View>
    </KeyboardAvoidingView>
  );
};

export default RegisterScreen;
