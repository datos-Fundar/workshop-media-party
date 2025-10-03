import litellm


class BaseAgent:
    name: str
    system_prompt: str

    def __init__(self, name: str, system_prompt: str = '', **kwargs):
        self.name = name
        self.system_prompt = system_prompt
        self.kwargs = kwargs

    def completion(self, prompt: str) -> str:
        messages = []
        if self.system_prompt:
            messages.append({"role": "system", "content": self.system_prompt})
        
        messages.append({"role": "user", "content": prompt})

        completions = litellm.completion(
            model=self.name,
            messages=messages,
            **self.kwargs
        )

        return completions['choices'][0]['message']['content']