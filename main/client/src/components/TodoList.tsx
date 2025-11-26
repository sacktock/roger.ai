import React from "react";
import type { Todo } from "../types";

interface Props {
  todos: Todo[];
  onToggle: (todo: Todo) => void;
  onDelete: (todo: Todo) => void;
}

export const TodoList: React.FC<Props> = ({ todos, onToggle, onDelete }) => {
  if (!todos.length) {
    return <p>No TODOs yet. Add one above!</p>;
  }

  return (
    <div>
      {todos.map((todo) => (
        <div className="todo-item" key={todo.id}>
          <div style={{ display: "flex", flexDirection: "column", flex: 1 }}>
            <span
              className={`todo-title ${false ? "completed" : ""}`}
              style={{ cursor: "pointer" }}
              onClick={() => onToggle(todo)}
            >
              {todo.text}
            </span>
          </div>
          <button
            className="secondary"
            style={{ marginLeft: "0.75rem" }}
            onClick={() => onDelete(todo)}
          >
            ✕
          </button>
        </div>
      ))}
    </div>
  );
};
