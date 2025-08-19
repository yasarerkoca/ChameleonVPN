export async function fetchTodo(token) {
  const response = await fetch('https://jsonplaceholder.typicode.com/todos/1', {
    headers: {
      Authorization: token ? `Bearer ${token}` : undefined,
    },
  });
  if (!response.ok) {
    throw new Error('Failed to fetch');
  }
  return response.json();
}
