import api from "./index";

export const uploadFile = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  return api.post("/pdf/upload/", formData);
};

export const getFiles = async () => api.get("/pdf/files/");

export const deleteFile = async (fileName) => api.delete(`/pdf/files/${fileName}`);

export const deleteAllFiles = async () => api.delete("/pdf/files/");