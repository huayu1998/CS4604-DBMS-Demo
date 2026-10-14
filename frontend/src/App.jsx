import { useEffect, useState } from "react";

const API = "http://127.0.0.1:5001/api/students";
const headers = { "Content-Type": "application/json" };
const empty = { name: "", major: "", gpa: "" };

export default function App() {
  const [students, setStudents] = useState([]);
  const [form, setForm] = useState(empty);
  const [editingId, setEditingId] = useState(null);

  const load = () => fetch(API).then(r => r.json()).then(setStudents);   // Read
  useEffect(() => { load(); }, []);

  const save = async (e) => {
    e.preventDefault();
    const body = JSON.stringify({ ...form, gpa: Number(form.gpa) });
    if (editingId) await fetch(`${API}/${editingId}`, { method: "PUT", headers, body }); // Update
    else await fetch(API, { method: "POST", headers, body });                            // Create
    setForm(empty);
    setEditingId(null);
    load();                                                              // refresh from DB
  };

  const edit = (s) => {
    setEditingId(s.studentID);
    setForm({ name: s.name, major: s.major ?? "", gpa: s.gpa ?? "" });
  };

  const remove = async (id) => {                                         // Delete
    await fetch(`${API}/${id}`, { method: "DELETE" });
    load();
  };

  const set = (field) => (e) => setForm({ ...form, [field]: e.target.value });

  return (
    <div>
      <h1>Students</h1>
      <form onSubmit={save}>
        <input placeholder="Name" value={form.name} onChange={set("name")} required />
        <input placeholder="Major" value={form.major} onChange={set("major")} />
        <input placeholder="GPA" type="number" step="0.01" min="0" max="4"
               value={form.gpa} onChange={set("gpa")} />
        <button>{editingId ? "Update" : "Add"}</button>
      </form>

      <table>
        <thead>
          <tr><th>ID</th><th>Name</th><th>Major</th><th>GPA</th><th></th></tr>
        </thead>
        <tbody>
          {students.map(s => (
            <tr key={s.studentID}>
              <td>{s.studentID}</td><td>{s.name}</td><td>{s.major}</td><td>{s.gpa}</td>
              <td>
                <button onClick={() => edit(s)}>Edit</button>{" "}
                <button onClick={() => remove(s.studentID)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}