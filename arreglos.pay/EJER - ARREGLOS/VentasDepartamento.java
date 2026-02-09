import java.util.Scanner;

public class VentasDepartamento {

    static double[][] ventas = {
        {120, 95, 80},   // Enero
        {110, 90, 75},   // Febrero
        {130, 100, 85},  // Marzo
        {140, 110, 90},  // Abril
        {150, 120, 100}, // Mayo
        {160, 130, 110}, // Junio
        {170, 140, 120}, // Julio
        {165, 135, 115}, // Agosto
        {155, 125, 105}, // Septiembre
        {180, 150, 130}, // Octubre
        {190, 160, 140}, // Noviembre
        {200, 170, 160}  // Diciembre
    };

    static String[] meses = {
        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    };

    static String[] departamentos = {"Ropa", "Deportes", "Juguetería"};

    static Scanner scanner = new Scanner(System.in);


    public static void insertarVenta(double[][] matriz) {
        System.out.print("Mes (1-12): ");
        int fila = scanner.nextInt() - 1;

        System.out.print("Departamento (1=Ropa, 2=Deportes, 3=Juguetería): ");
        int columna = scanner.nextInt() - 1;

        System.out.print("Nueva venta: ");
        double valor = scanner.nextDouble();

        matriz[fila][columna] = valor;
        System.out.println("Venta insertada correctamente.");
    }

    public static void buscarVenta(double[][] matriz) {
        System.out.print("Ingrese la venta a buscar: ");
        double valor = scanner.nextDouble();
        boolean encontrado = false;

        for (int i = 0; i < matriz.length; i++) {
            for (int j = 0; j < matriz[i].length; j++) {
                if (matriz[i][j] == valor) {
                    System.out.println("Venta encontrada en " 
                        + meses[i] + " - " + departamentos[j]);
                    encontrado = true;
                }
            }
        }

        if (!encontrado) {
            System.out.println("La venta no fue encontrada.");
        }
    }

    public static void eliminarVenta(double[][] matriz) {
        System.out.print("Mes (1-12): ");
        int fila = scanner.nextInt() - 1;

        System.out.print("Departamento (1=Ropa, 2=Deportes, 3=Juguetería): ");
        int columna = scanner.nextInt() - 1;

        matriz[fila][columna] = 0;
        System.out.println("Venta eliminada correctamente.");
    }

    public static void mostrarTabla(double[][] matriz) {
        System.out.printf("\n%-12s%12s%12s%14s\n", 
                "Mes", "Ropa", "Deportes", "Juguetería");
        System.out.println("--------------------------------------------------");

        for (int i = 0; i < matriz.length; i++) {
            System.out.printf("%-12s", meses[i]);
            for (int j = 0; j < matriz[i].length; j++) {
                System.out.printf("%12.2f", matriz[i][j]);
            }
            System.out.println();
        }
    }

    public static void main(String[] args) {

        int opcion;

        do {
            System.out.println("\n--- MENÚ DE OPCIONES ---");
            System.out.println("1. Insertar venta");
            System.out.println("2. Buscar venta");
            System.out.println("3. Eliminar venta");
            System.out.println("4. Mostrar tabla");
            System.out.println("5. Salir");
            System.out.print("Seleccione una opción: ");

            opcion = scanner.nextInt();

            switch (opcion) {
                case 1:
                    insertarVenta(ventas);
                    break;
                case 2:
                    buscarVenta(ventas);
                    break;
                case 3:
                    eliminarVenta(ventas);
                    break;
                case 4:
                    mostrarTabla(ventas);
                    break;
                case 5:
                    System.out.println("Saliendo del programa...");
                    break;
                default:
                    System.out.println("Opción no válida, intente de nuevo.");
            }

        } while (opcion != 5);
    }
}
