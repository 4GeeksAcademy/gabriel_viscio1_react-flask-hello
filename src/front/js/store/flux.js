const getState = ({ getStore, getActions, setStore }) => {
    return {
        store: {
            user: null, 
            token: sessionStorage.getItem('token') || null,
        },
        actions: {
            signup: async (email, password) => {
                const resp = await fetch(`https://crispy-trout-7vrvp9j75r6rfprq7-3001.app.github.dev/api/signup`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email, password })
                });
                if (resp.ok) {
                    const data = await resp.json();
                    console.log('Usuario registrado con éxito:', data);
                    return true;
                } else {
                    console.error('Error al registrar usuario');
                    return false;
                }
            },
            login: async (email, password) => {
                const resp = await fetch(`https://crispy-trout-7vrvp9j75r6rfprq7-3001.app.github.dev/api/login`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email, password })
                });
                if (resp.ok) {
                    const data = await resp.json();
                    sessionStorage.setItem('token', data.token);
                    setStore({ token: data.token });
                    window.location.href="/private"
                    return true;
                } else {
                    console.error('Error al iniciar sesión');
                    return false;
                }
            },
            validateToken: async () => {
                const token = getStore().token;
                const resp = await fetch('https://crispy-trout-7vrvp9j75r6rfprq7-3001.app.github.dev/api/validate', {
                    method: 'GET',
                    headers: { Authorization: `Bearer ${token}` }
                });
                if (resp.ok) {
                    const data = await resp.json();
                    setStore({ user: data });
                    return true;
                } else {
                    console.error('Token inválido');
                    return false;
                }
            },
            logout: () => {
                sessionStorage.removeItem('token');
                setStore({ token: null, user: null });
            }
        }
    };
};

export default getState;
