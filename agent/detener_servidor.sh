#!/bin/bash
# Script para detener el servidor GUI del agente

echo "🛑 Deteniendo servidor GUI del agente..."
echo ""

# Buscar y detener procesos de Python relacionados con el agente
PYTHON_PROCS=$(ps aux | grep -E "run_agent.py.*gui-server|python.*gui-server" | grep -v grep | awk '{print $2}')

if [ -n "$PYTHON_PROCS" ]; then
    echo "📌 Procesos de Python encontrados: $PYTHON_PROCS"
    echo "$PYTHON_PROCS" | xargs kill 2>/dev/null
    sleep 1
    
    # Verificar si aún están corriendo
    REMAINING=$(ps aux | grep -E "run_agent.py.*gui-server|python.*gui-server" | grep -v grep | awk '{print $2}')
    if [ -n "$REMAINING" ]; then
        echo "⚠️  Forzando detención..."
        echo "$REMAINING" | xargs kill -9 2>/dev/null
        sleep 1
    fi
    echo "✅ Procesos de Python detenidos"
fi

# Buscar procesos en puertos comunes (8080-8085)
for PORT in 8080 8081 8082 8083 8084 8085; do
    PORT_PID=$(lsof -ti :$PORT 2>/dev/null)
    if [ -n "$PORT_PID" ]; then
        echo "📌 Proceso encontrado en puerto $PORT: PID $PORT_PID"
        kill $PORT_PID 2>/dev/null
        sleep 1
        
        # Verificar si se detuvo
        if lsof -ti :$PORT > /dev/null 2>&1; then
            echo "⚠️  Forzando detención en puerto $PORT..."
            kill -9 $PORT_PID 2>/dev/null
            sleep 1
        fi
        
        if ! lsof -ti :$PORT > /dev/null 2>&1; then
            echo "✅ Puerto $PORT liberado"
        fi
    fi
done

# Verificación final
REMAINING_PROCS=$(ps aux | grep -E "run_agent.py.*gui-server|python.*gui-server" | grep -v grep)
REMAINING_PORTS=$(lsof -ti :8080,8081,8082,8083,8084,8085 2>/dev/null)

if [ -z "$REMAINING_PROCS" ] && [ -z "$REMAINING_PORTS" ]; then
    echo ""
    echo "✅ Limpieza completada. Todos los servidores detenidos."
    echo ""
    echo "Ahora puedes iniciar el servidor con:"
    echo "   ./run.sh gui-server"
else
    echo ""
    echo "⚠️  Algunos procesos aún pueden estar corriendo:"
    [ -n "$REMAINING_PROCS" ] && echo "$REMAINING_PROCS"
    [ -n "$REMAINING_PORTS" ] && echo "Puertos ocupados: $REMAINING_PORTS"
fi

