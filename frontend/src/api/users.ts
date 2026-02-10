import api from "./http";

export async function searchUsers(query: string) {
  if (!query.trim()) return [];
  const { data } = await api.get(
    `/users/search?q=${encodeURIComponent(query)}`
  );

  console.log("data", data);
  return data.results;
}

export async function getRecentUsers() {
  const { data } = await api.get("/users/recent");
  // backend returns an array directly
  return Array.isArray(data) ? data : [];
}

export async function fetchEmotionStats() {
  const { data } = await api.get("/users/emotion-stats");
  // backend returns an array directly
  return data;
}

export async function profileUpload(formData: FormData) {
  const token = localStorage.getItem("access_token");

  const { data } = await api.post("/users/profile-picture", formData, {
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "multipart/form-data",
    },
  });

  console.log("data", data);

  localStorage.setItem("profile_picture", data.url);
  return data.url;
}
