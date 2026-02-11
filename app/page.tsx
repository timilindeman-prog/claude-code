export default function Home() {
  return (
    <main>
      <h1>App Generator</h1>

      <label htmlFor="app-description">Describe the app you want</label>
      <textarea
        id="app-description"
        name="app-description"
        rows={6}
        placeholder="Describe your app idea..."
      />

      <button type="button">Generate</button>

      <div className="output-area" aria-live="polite" />
    </main>
  );
}
