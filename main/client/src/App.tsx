import React, { useEffect, useState } from "react";
import axios from "axios";
import type { Project, Todo } from "./types";
import { ProjectSelector } from "./components/ProjectSelector";
import { TodoList } from "./components/TodoList";

const BACKEND_URL = "http://localhost:8000";
const user_id = 1;

function App() {

    const [projects, setProjects] = useState<Project[]>([]);
    const [selectedProjectId, setSelectedProjectId] = useState<number | null>(
        null
    );
    const [todos, setTodos] = useState<Todo[]>([]);
    const [user, setUser] = useState<string>("");
    const [projectName, setProjectName] = useState<string>("");
    const [projectDescription, setProjectDescription] = useState<string>("");
    const [requestBody, setRequestBody] = useState<string>("");
    const [responseBody, setResponseBody] = useState<string>("");
    const [loading, setLoading] = useState<boolean>(false);

    useEffect(() => {
        (async () => {
            setLoading(true);
            try {
                await loadContent();
            } finally {
                setLoading(false);
            }
        })();
    }, [])

    const loadContent = async () => {
        console.log("Loading content")
        try {
            const response = await axios.get(`${BACKEND_URL}/users/${user_id}/projects/todos`);
            //setUser("UNKNOWN USER");
            setUser(`${response.data.name}`);
            setProjects(response.data.projects);
            if (!selectedProjectId && response.data.projects.length > 0) {
                setTodos(response.data.projects[0].todos);
                setSelectedProjectId(response.data.projects[0].id)
            }
        } catch (error: any) {
            console.error("Error loading content", error?.response || error?.message || error);
            setUser("Error loading content");
        }
    }

    const makeRequest = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        try {
            const response = await axios.get(`${BACKEND_URL}/roger/request`, {params: {text: requestBody}});
            setResponseBody(response.data.text);
        } catch (error: any) {
            console.error("Error making request to roger.ai", error?.response || error?.message || error);
            setResponseBody("Error making request to roger.ai");
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className="app-root">
            <div className="card">
                <h1>Hello {user}!</h1>
                    <p style={{ opacity: 0.7, fontSize: "0.9rem" }}>
                    Welcome to roger.ai your personal project manager! Manage projects and tasks by making requests via the chat bar!
                    </p>
                <form
                    onSubmit={makeRequest}
                    style={{
                        display: "flex",
                        flexWrap: "wrap",
                        gap: "0.5rem",
                        marginBottom: "0.75rem"
                    }}
                >
                    <input
                        placeholder="How can I help you today?"
                        value={requestBody}
                        onChange={(e) => setRequestBody(e.target.value)}
                        style={{ flex: "1 1 180px" }}
                        disabled={loading}
                    />
                    <button type="submit" disabled={loading}>
                        Send Request
                    </button>
                </form>
                <p style={{ opacity: 0.7, fontSize: "0.9rem" }}>
                    {responseBody}
                </p>
                <h2 style={{ marginTop: "1.5rem" }}>Projects</h2>
                <form
                onSubmit={() => {}}
                style={{
                    display: "flex",
                    flexWrap: "wrap",
                    gap: "0.5rem",
                    marginBottom: "0.75rem"
                }}
                >
                    <input
                        placeholder="New project name"
                        value={projectName}
                        onChange={(e) => setProjectName(e.target.value)}
                        style={{ flex: "1 1 180px" }}
                        disabled={loading}
                    />
                    <input
                        placeholder="Optional description"
                        value={projectDescription}
                        onChange={(e) => setProjectDescription(e.target.value)}
                        style={{ flex: "2 1 240px" }}
                        disabled={loading}
                    />
                    <button type="submit" disabled={loading}>
                        Add Project
                    </button>
                </form>

                <ProjectSelector
                    projects={projects}
                    selectedProjectId={selectedProjectId}
                    onSelect={setSelectedProjectId}
                    />

                <h2>TODOs</h2>
                {!selectedProjectId && (
                <p style={{ fontSize: "0.9rem", opacity: 0.7 }}>
                    Select or create a project to start adding TODOs.
                </p>
                )}

                <TodoList
                todos={todos}
                onToggle={() => {}}
                onDelete={() => {}}
                />

                {loading && (
                <p style={{ marginTop: "1rem", fontSize: "0.8rem", opacity: 0.7 }}>
                    Working...
                </p>
                )}
            </div>
        </div>
    );
}

export default App;