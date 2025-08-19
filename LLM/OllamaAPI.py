import requests
import json
import queue


class OllamaAPI:
    """OLLAMA API interface class"""
    
    # OLLAMA configuration - using qwen3:8b model
    OLLAMA_URL = "http://localhost:11434/api/generate"
    OLLAMA_MODEL = "qwen3:8b"

    def __init__(self, model_name: str = "qwen3:8b"):
        """
        Initialize the Ollama API client
        
        Args:
            model_name (str): Name of the model to use (default: qwen3:8b)
        """
        self.model_name = model_name
        self.url = self.OLLAMA_URL
        print(f"Initializing OLLAMA API with model: {self.model_name}")

    def generate_response_stream(self, prompt: str, system_prompt: str, response_queue: queue.Queue):
        """
        Streamed call to OLLAMA API to generate responses - with Chinese encoding support
        
        Args:
            prompt (str): User input prompt
            system_prompt (str): System-level instruction/prompt
            response_queue (queue.Queue): Thread-safe queue to send response chunks
        """
        try:
            print(f"Sending streaming request to OLLAMA (Model: {self.model_name})")
            
            # Prepare the request payload
            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "system": system_prompt,
                "stream": True,  # Enable streaming response
                "options": {
                    "temperature": 0.7,    # Controls randomness (higher = more creative)
                    "top_p": 0.9,          # Nucleus sampling threshold
                    "repeat_penalty": 1.1  # Reduce repetition
                }
            }

            # Make POST request with proper headers and streaming enabled
            response = requests.post(
                self.url,
                json=payload,
                timeout=120,  # 2-minute timeout
                stream=True,
                headers={'Content-Type': 'application/json; charset=utf-8'}
            )

            if response.status_code == 200:
                full_response = ""
                # Process each line in the streamed response
                for line in response.iter_lines(decode_unicode=True):
                    if line:  # Skip empty lines
                        try:
                            data = json.loads(line)
                            
                            # If response chunk is received, add to output
                            if 'response' in data:
                                chunk = data['response']
                                full_response += chunk
                                response_queue.put(('chunk', chunk))
                            
                            # If generation is complete, send final message
                            elif 'done' in data and data['done']:
                                response_queue.put(('done', full_response))
                                break
                                
                        except json.JSONDecodeError:
                            # Skip malformed JSON lines
                            continue
            else:
                error_msg = f"API request failed: {response.status_code}"
                response_queue.put(('error', error_msg))

        except requests.exceptions.Timeout:
            response_queue.put(('error', 'API request timed out'))
        except requests.exceptions.RequestException as e:
            response_queue.put(('error', f'Network request error: {e}'))
        except Exception as e:
            response_queue.put(('error', f'API call error: {e}'))