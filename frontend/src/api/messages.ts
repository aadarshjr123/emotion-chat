import api from "./http";

export async function getHistory(otherUserId: number) {
  const { data } = await api.get(`/messages/history/${otherUserId}`);
  return data;
}
