export interface Project {
  id: number;
  name: string;
  description?: string | null;
}

export interface Todo {
  id: number;
  text: string;
}