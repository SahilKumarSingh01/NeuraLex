export const sendMessage = async (text, files, mode) => {
  const res = await axios.post("http://localhost:8000/chat", {
    question: text,
    files,
    mode
  });
  return res.data;
};