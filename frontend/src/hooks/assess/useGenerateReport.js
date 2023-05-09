import axios from 'axios'
import { ref, onMounted } from 'vue'

export function getChatGPTReport() {
	const generatedGPTText = ref([]);
  const isGPTTextLoading = ref(false);
	const fetchChatGPTReport = async (text) => {
    const prompt = "Напиши отзыв об ученике в 3 предложениях";
		const apiKey = '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';
    const apiUrl = 'https://api.openai.com/v1/completions';
    const data = {
      prompt: prompt,
      model: "text-davinci-003",
      max_tokens: 500, // Максимальное количество токенов в ответе
      temperature: 0.7, // Параметр, контролирующий "творчество" ответов (чем выше значение, тем более случайными будут ответы)
      n: 1, // Количество вариантов ответов, которые API вернет в ответе
    };
    const config = {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey}`
      }
    }
    isGPTTextLoading.value = true;
		await axios.post(apiUrl, data, config).then((response) => {
			console.log("Генерация текста")
      console.log(response.data)
      const { choices } = response.data;
      const [reply] = choices;
			generatedGPTText.value = reply.text.trim()
			console.log(generatedGPTText.value)
		}).finally(() => {
      isGPTTextLoading.value = false;
    });
	};
	return {
		generatedGPTText, isGPTTextLoading, fetchChatGPTReport
	}
}
