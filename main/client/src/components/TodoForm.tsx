import React, { useState } from "react";

interface Props {
  disabled?: boolean;
  onCreate: (data: {
    title: string;
    description?: string;
    due_date?: string | null;
  }) => Promise<void>;
}

export const TodoForm: React.FC<Props> = ({ disabled, onCreate }) => {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [dueDate, setDueDate] = useState<string>("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) return;
    await onCreate({
      title: title.trim(),
      description: description.trim() || undefined,
      due_date: dueDate || null
    });
    setTitle("");
    setDescription("");
    setDueDate("");
  };

  return (
    <form
      onSubmit={handleSubmit}
      style={{
        display: "flex",
        flexDirection: "column",
        gap: "0.5rem",
        marginBottom: "1rem"
      }}
    >
      <input
        placeholder="New TODO title"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        disabled={disabled}
      />
      <textarea
        placeholder="Optional description"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        rows={2}
        disabled={disabled}
      />
      <div style={{ display: "flex", gap: "0.5rem", alignItems: "center" }}>
        <label style={{ fontSize: "0.85rem" }}>
          Due date:
          <input
            type="date"
            value={dueDate}
            onChange={(e) => setDueDate(e.target.value)}
            style={{ marginLeft: "0.3rem" }}
            disabled={disabled}
          />
        </label>
        <button type="submit" disabled={disabled}>
          Add TODO
        </button>
      </div>
    </form>
  );
};
