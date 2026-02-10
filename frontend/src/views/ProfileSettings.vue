<template>
  <div class="profile-container">
  <div class="profile-card">
  <div class="profile-settings">
    <h3>Upload Profile Picture</h3>
    <FileUpload
      name="file"
      url="/api/users/profile-picture"
      accept="image/*"
      @uploader="onUpload"
      :customUpload="true"
      :multiple="false"                    
      :auto="false" 
      :chooseLabel="'Upload Image'"
      :uploadLabel="'Upload Now'"
    />
    <!-- <img v-if="imageUrl" :src="imageUrl" class="preview" /> -->
  </div>
  </div>
  </div>
</template>

<script setup lang="ts">
import FileUpload from 'primevue/fileupload';
import { ref } from 'vue';
import { profileUpload } from '../api/users';
import { useRouter } from 'vue-router';

const imageUrl = ref("");
const router = useRouter();


async function onUpload(event: any) {
  const file = event.files[0];
  const formData = new FormData();
  formData.append("file", file);

  try {
    const res = await profileUpload(formData); // must return { url: "/static/uploads/xyz.jpg" }
    const uploadedUrl = res;

    // ✅ Update localStorage & emit event
    localStorage.setItem("profile_picture", uploadedUrl);
    imageUrl.value = uploadedUrl;

    // ✅ Dispatch a browser event to update header globally
    window.dispatchEvent(new CustomEvent("profile-updated", { detail: uploadedUrl }));
    router.push("/home"); // 🚀 Redirect
  } catch (err) {
    console.error("Upload failed:", err);
    imageUrl.value = "";
  }
}
</script>

<style scoped>

.profile-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 50vh;
  background-color: var(--surface-ground);
  padding: 1.5rem;
}

.profile-card {
  background: var(--surface-card);
  border-radius: 10px;
  width: 100%;
  max-width: 700px;
  height: 80vh;
  display: flex;
  flex-direction: column;
}
.preview {
  margin-top: 1rem;
  width: 100px;
  height: 100px;
  border-radius: 50%;
}
</style>
