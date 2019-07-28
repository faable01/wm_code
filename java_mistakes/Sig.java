package java_mistakes;
import java_mistakes.Human;

public class Sig extends Human {
    private String address;
    public Sig(String name, int age, String address) {
        super(name, age);
        this.address = address;
    }
    public void talk() {
        // System.out.println("'name' is " + this.name + ", 'address' is " + this.address);
        // ▲コンパイルエラー：The field Human.name is not visible
    }
    public void plusOneCurrentAge() {
        // super.age += 1;
        // System.out.println(super.age);
        // ▲コンパイルエラー：The field Human.age is not visible
    }
}