import logo from './logo.svg';
import './App.css';
import NoteList from './components/NoteList';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          View the source code for this project.
        </p>
        <a
          className="App-link"
          href="https://github.com/bahim22/engage_flower"
          target="_blank"
          rel="noopener noreferrer"
        >
          Hima GitHub Profile
        </a>
      </header>
	  <NoteList />
    </div>
  );
}

export default App;
