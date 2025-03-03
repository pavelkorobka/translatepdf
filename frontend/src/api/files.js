import api from "./index";
import { getAccessToken } from "../utils/authHelper"; 

export const uploadFile = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  return api.post("/pdf/upload/", formData, {
    headers: { Authorization: `Bearer ${getAccessToken()}` },
  });
};

export const getFiles = async () =>
  api.get("/pdf/files/", {
    headers: { Authorization: `Bearer ${getAccessToken()}` },
  });

export const deleteFile = async (fileName) =>
  api.delete(`/pdf/files/${fileName}`, {
    headers: { Authorization: `Bearer ${getAccessToken()}` },
  });

export const deleteAllFiles = async () =>
  api.delete("/pdf/files/", {
    headers: { Authorization: `Bearer ${getAccessToken()}` },
  });