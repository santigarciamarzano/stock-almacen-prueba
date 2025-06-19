import { useState, useEffect } from 'react';
import './App.css';

const API_BASE_URL = 'http://localhost:8000/api';

function App() {
  const [items, setItems] = useState([]);
  const [movements, setMovements] = useState([]);
  const [error, setError] = useState(null);

  // --- Lógica de Datos ---

  const fetchData = async () => {
    try {
      const [itemsResponse, movementsResponse] = await Promise.all([
        fetch(`${API_BASE_URL}/items/`),
        fetch(`${API_BASE_URL}/movements/`)
      ]);

      if (!itemsResponse.ok || !movementsResponse.ok) {
        throw new Error('Error al obtener los datos del servidor.');
      }

      const itemsData = await itemsResponse.json();
      const movementsData = await movementsResponse.json();

      setItems(itemsData);
      setMovements(movementsData);
      setError(null);
    } catch (err) {
      console.error("Error en fetchData:", err);
      setError("No se pudo conectar con el servidor. ¿Está el backend funcionando?");
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  // --- Funciones de Interacción con la API ---

  const handleUpdateStock = async (itemId) => {
    const newStockString = prompt("Introduce la NUEVA CANTIDAD TOTAL de stock:");
    if (!newStockString) return;

    const newStock = parseInt(newStockString, 10);
    if (isNaN(newStock) || newStock < 0) {
      alert("Por favor, introduce un número válido y no negativo.");
      return;
    }

    const currentItem = items.find(item => item.id === itemId);
    if (!currentItem) return;
    
    const changeAmount = newStock - currentItem.stock;
    await adjustStockOnServer(itemId, changeAmount);
  };

  const handleAdjustStock = async (itemId) => {
    const amountString = prompt("Introduce la cantidad a AJUSTAR (ej: 10 para añadir, -5 para quitar):");
    if (!amountString) return;

    const changeAmount = parseInt(amountString, 10);
    if (isNaN(changeAmount)) {
      alert("Por favor, introduce un número válido.");
      return;
    }

    await adjustStockOnServer(itemId, changeAmount);
  };

  const adjustStockOnServer = async (itemId, change) => {
    try {
      const response = await fetch(`${API_BASE_URL}/items/${itemId}/adjust`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ change: change }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Error al ajustar el stock.');
      }
      await fetchData();
    } catch (err) {
      console.error("Error en adjustStockOnServer:", err);
      alert(`Error: ${err.message}`);
    }
  };

  // NUEVA FUNCIÓN: Lógica para limpiar el historial de movimientos.
  const handleClearHistory = async () => {
    // Se pide confirmación al usuario antes de una acción destructiva.
    if (!window.confirm("¿Estás seguro de que quieres borrar todo el historial de movimientos? Esta acción no se puede deshacer.")) {
      return;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/movements/`, {
        method: 'DELETE',
      });

      // El código 204 (No Content) también es una respuesta de éxito para DELETE.
      if (!response.ok && response.status !== 204) {
        throw new Error('Error al limpiar el historial.');
      }

      // Refrescamos los datos para que la lista de movimientos se vacíe en la UI.
      await fetchData();
    } catch (err) {
      console.error("Error en handleClearHistory:", err);
      alert(`Error: ${err.message}`);
    }
  };


  // --- Renderizado del Componente ---

  return (
    <div className="App">
      <header>
        <h1>Gestión de Inventario</h1>
      </header>

      {error && <p className="error-message">{error}</p>}

      <main>
        <section>
          <h2>Stock Actual</h2>
          <table>
            <thead>
              <tr>
                <th>SKU</th>
                <th>EAN13</th>
                <th>Stock</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              {items.map(item => (
                <tr key={item.id}>
                  <td>{item.sku}</td>
                  <td>{item.ean13}</td>
                  <td>{item.stock}</td>
                  <td className="actions">
                    <button onClick={() => handleUpdateStock(item.id)}>
                      Establecer
                    </button>
                    <button onClick={() => handleAdjustStock(item.id)}>
                      Ajustar (+/-)
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>

        <section>
          <div className="history-header">
            <h2>Historial de Movimientos</h2>
            {/* El botón de limpiar solo se muestra si hay movimientos en la lista. */}
            {movements.length > 0 && (
              <button onClick={handleClearHistory} className="clear-history-btn">
                Limpiar Historial
              </button>
            )}
          </div>
          <ul>
            {movements.length > 0 ? (
              movements.map(movement => (
                <li key={movement.id}>
                  {new Date(movement.timestamp).toLocaleString()} - 
                  Item ID: {movement.item_id} - 
                  Cambio: {movement.change > 0 ? `+${movement.change}` : movement.change}
                </li>
              ))
            ) : (
              <li>No hay movimientos registrados.</li>
            )}
          </ul>
        </section>
      </main>
    </div>
  );
}

export default App;