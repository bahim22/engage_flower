import './App.css';
import FilterButton from './compos/FilterButton';
import Form from './compos/Form';
import Todo from './compos/Todo';
// import MainNav from './components/Main';


function App() {
	return (
		<>
			<Form />
			<Todo />
			<FilterButton />
		</>
	)
}




/* import logo from './logo.svg';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

*/
export default App;
