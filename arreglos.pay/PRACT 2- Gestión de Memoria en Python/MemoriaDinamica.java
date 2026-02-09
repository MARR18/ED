import java.util.ArrayList;

public class MemoriaDinamica {

    public static void main(String[] args) {
        ArrayList<String> frutas=new ArrayList<>();
        frutas.add("Mango");
        frutas.add("Manzana");
        frutas.add("Bananas");
        frutas.add("Uvas");
        System.out.println(frutas);
        frutas.remove(0);
        frutas.remove(1);
        frutas.add("Sandia");
        System.out.println(frutas);
    }
}