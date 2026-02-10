import api from "./http";

export async function loginUser(username: string, password: string) {
  const { data } = await api.post("/auth/login", { username, password });
  console.log("login", data);
  localStorage.setItem("access_token", data.access_token);
  return data;
}

export async function registerUser(username: string, password: string) {
  return api.post("/auth/signup", { username, password });
}

export function logout() {
  localStorage.removeItem("access_token");
}
