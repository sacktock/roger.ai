import React from "react";
import type { Project } from "../types";

interface Props {
  projects: Project[];
  selectedProjectId: number | null;
  onSelect: (id: number | null) => void;
}

export const ProjectSelector: React.FC<Props> = ({
  projects,
  selectedProjectId,
  onSelect
}) => {
  return (
    <div style={{ marginBottom: "1rem" }}>
      <label>
        <span style={{ marginRight: "0.5rem" }}>Project:</span>
        <select
          value={selectedProjectId ?? ""}
          onChange={(e) =>
            onSelect(e.target.value ? Number(e.target.value) : null)
          }
        >
          <option value="">All projects</option>
          {projects.map((p) => (
            <option key={p.id} value={p.id}>
              {p.name}
            </option>
          ))}
        </select>
      </label>
    </div>
  );
};
