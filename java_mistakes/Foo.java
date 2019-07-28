package java_mistakes;

private class Foo {
    public Foo() {
        System.out.println("コンストラクタ実行");
    }
    {
        System.out.println("イニシャライザ実行");
    }
}