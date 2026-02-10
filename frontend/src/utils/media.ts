export const API_BASE =
  import.meta.env.VITE_API_BASE || "http://localhost:8000";

export function toMediaUrl(path?: string | null) {
  if (!path) return "";
  // If backend already returns a full URL, keep it
  if (path.startsWith("http://") || path.startsWith("https://")) return path;

  // Ensure exactly ONE slash between base and path
  const cleanBase = API_BASE.replace(/\/+$/, "");
  const cleanPath = path.startsWith("/") ? path : `/${path}`;

  return `${cleanBase}${cleanPath}`;
}
