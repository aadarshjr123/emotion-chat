import { ref, computed } from "vue";
import { useRouter } from "vue-router";
import { loginUser, registerUser } from "../api/auth";
import { useChat } from "./useChat";
import { jwtDecode } from "jwt-decode";
import api from "../api/http";

const token = ref<string | null>(localStorage.getItem("access_token"));
const userId = ref<number | null>(
  Number(localStorage.getItem("user_id")) || null,
);
const username = ref<string | null>(localStorage.getItem("username"));
const profilePicture = ref<string>(
  localStorage.getItem("profile_picture") || "",
);

export function useAuth() {
  const router = useRouter();

  async function login(usernameInput: string, password: string) {
    const data = await loginUser(usernameInput, password);
    const decoded: any = jwtDecode(data.access_token);
    const id = Number(decoded.sub);
    // const profile_picture = decoded.profile_picture;

    token.value = data.access_token;
    userId.value = id;
    username.value = usernameInput;
    const profile_picture = decoded.profile_picture || "";
    const normalized = profile_picture.startsWith("/")
      ? profile_picture
      : `/${profile_picture}`;

    profilePicture.value = normalized;

    localStorage.setItem("access_token", data.access_token);
    localStorage.setItem("user_id", id.toString());
    localStorage.setItem("username", usernameInput);
    localStorage.setItem("profile_picture", normalized);
    // localStorage.setItem("profile_picture", "/" + profile_picture);
    router.push("/home");
  }

  async function register(usernameInput: string, password: string) {
    try {
      const res = await registerUser(usernameInput, password);
      console.log("Signup response:", res);

      if (res.status === 200 || res.status === 201) {
        await login(usernameInput, password);
      } else {
        console.error("Unexpected signup status:", res.status);
        alert("Registration failed: unexpected server response");
      }
    } catch (err: any) {
      console.error("Registration failed:", err.response?.data || err);
      alert(
        "Registration failed: " +
          (err.response?.data?.detail || err.message || "Unknown error"),
      );
    }
  }

  function logout() {
    const { disconnect } = useChat();
    disconnect();
    token.value = null;
    userId.value = null;
    username.value = null;
    profilePicture.value = "";
    localStorage.removeItem("access_token");
    localStorage.removeItem("user_id");
    localStorage.removeItem("username");
    localStorage.removeItem("profile_picture");
    localStorage.removeItem("last_chat_user");
    localStorage.removeItem("last_chat_username");
    router.push("/login");
  }

  return {
    token,
    userId,
    username,
    profilePicture: computed(() => profilePicture.value),
    login,
    register,
    logout,
  };
}
