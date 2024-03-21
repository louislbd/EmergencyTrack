import Router from "./router/Router";
import { AuthProvider } from "./context/Auth";
function App() {
  return (
    <div className="App">
      <header className="App-header"></header>
      <AuthProvider>
        <Router />
      </AuthProvider>
    </div>
  );
}

export default App;
