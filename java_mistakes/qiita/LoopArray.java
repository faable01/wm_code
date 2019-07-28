package java_mistakes.qiita;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.LinkedList;
import java.util.List;
import java.util.ListIterator;
/**
 * 参考：https://docs.oracle.com/javase/jp/1.3/api/java/util/AbstractList.html#modCount
 * modCount
 * protected transient int modCount
 * このリストの「構造が変更された」回数です。構造の変更とは、リストのサイズの変更や、その他の進行中の繰り返し処理が不正な結果をもたらすような変更のことです。
 * このフィールドは、iterator メソッドおよび listIterator メソッドによって返される反復子およびリスト反復子の実装によって使用されます。このフィールドの値が予期しない形で変化した場合、反復子やリスト反復子は next、remove、previous、set、または add のオペレーションに応じて ConcurrentModificationException をスローします。これは、繰り返し処理中の同時変更を前にして、未確定動作ではなくフェイルファスト動作を提供します。

 * このフィールドをサブクラスで使用するのは任意です。サブクラスでフェイルファスト反復子およびリスト反復子を提供する必要がある場合には、単純に、サブクラスの add(int, Object) メソッドおよび remove(int) メソッド (および、サブクラスがオーバーライドするメソッドのうちで、リストの構造的な変更をするメソッド) の内部で、このフィールドをインクリメントします。add(int, Object) または remove(int) に対する 1 回の呼び出しでは、フィールドに 1 だけ加える必要があります。そうしないと、反復子 (およびリスト反復子) が誤って ConcurrentModificationExceptions をスローすることになります。実装でフェイルファスト反復子を提供しない場合は、このフィールドを無視してもかまいません。
 */
public class LoopArray {

    public static void main(String[] args) {

        List<String> list = new ArrayList<>(Arrays.asList("foo", "hoo", "hoge"));
        // for (String str : list) {
        //     list.add(str);
        // }

        list.stream().forEach(list::add);

        // イテレータの内部からならok?
        // for (ListIterator<String> itr = list.listIterator(); itr.hasNext();) {
        //     String str = itr.next();
        //     itr.add(str + "_itr");
        // }
        // list: [foo, foo_itr, hoo, hoo_itr, hoge, hoge_itr]
        // previous方向にaddが要素追加のため、無限ループにはならない
        
        System.out.println(list);

        // 他のリスト系クラスもだめ
        // LinkedList<String> l = new LinkedList<>(Arrays.asList("foo", "hoo", "hoge"));
        // l.stream().forEach(l::add);
        // System.out.println(l);
    }
}

/**
 * ListIterator.add()
 * 
 * Inserts the specified element into the list (optional operation).
 * The element is inserted immediately before the element that
 * would be returned by {@link #next}, if any, and after the element
 * that would be returned by {@link #previous}, if any.  (If the
 * list contains no elements, the new element becomes the sole element
 * on the list.)  The new element is inserted before the implicit
 * cursor: a subsequent call to {@code next} would be unaffected, and a
 * subsequent call to {@code previous} would return the new element.
 * (This call increases by one the value that would be returned by a
 * call to {@code nextIndex} or {@code previousIndex}.)
 * 
 * #### Google翻訳
 * 指定された要素をリストに挿入します（オプションの操作）。
 * 要素は、{@ link #next}によって返される要素の直前に（存在する場合）、
 * および{@link #previous}によって返される要素の直後に挿入されます（存在する場合）。 
 * （リストに要素が含まれていない場合は、新しい要素がリストの唯一の要素になります。）
 * 新しい要素は暗黙のカーソルの前に挿入されます。
 * それ以降の{@code next}の呼び出しは影響を受けません。 
 * code previous}は新しい要素を返します。 
 * （この呼び出しは、{@ code nextIndex}または{@code previousIndex}への呼び出しによって返される値を1つ増やします。）
 */