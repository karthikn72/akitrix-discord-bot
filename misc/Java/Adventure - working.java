/*
runAway() = escape




*/


import java.util.Random;
import java.util.Scanner;

public class Adventure {

    private final static Scanner scan = new Scanner(System.in);

    private static int points = 20, gold = 100, health = 100, morale = 50, weaponDmg = 0, level = 0;

    private static String Potion = "no potion";

    private static Random rand = new Random();

    public static void main(String[] args) {
        String shopType;
        String currentOption;
        int healthLoss;
        int goldLost;
        int earnedPoints;
        int monsterEncounter;
        int monsterDamage;
        int monsterHealth;
        int secret;

        print("You have " + getPoints() + " points, this will be your levelling system, do you understand? Y/N");
        currentOption = scan.next();

        if (currentOption ==("Yes")) {
            print("You may continue with your adventure!");
        } else {
            print("We're going to continue anyways.");
        }
        print("While walking through the woods something jumps out of the bushes!");
        print("Its a wild boar, and it doesnt look happy!");
        print("Do you want to run or fight?");

        currentOption = scan.next();
             if (currentOption ==("fight")) {
               fight(currentOption);
               }

                 else if (currentOption ==("run")) {
                        runAway(currentOption);
                 }



            print("You notice there is a village up ahead...");
            print("Do you want to go to the village? (Y/N)");
            currentOption = scan.next();

        if (currentOption ==("Yes")) {
            print("You notice that there's a few shops after entering the village.");
            print("You see a potion shop, a weapons shop, and an armor shop. Would you like to go to one? Y/N");
            currentOption = scan.next();

            while (currentOption ==("Yes")) {
               print("Which shop would you like to go to?");
               openShop(currentOption = scan.next());
               print("Would you like to go to another shop? Y/N");
               currentOption = scan.next();
               }

              print("You begin to leave the town and notice a bounty board for hunting down a monster");
              print("You decide to take up this task on defeating the monster and set out into the woods");
              }
              else if (currentOption ==("No")){
              print("You decide to continue traveling through the woods");
              }
              print("While in the woods you begin to here a rustling noise");
               monsterEncounter = rand.nextInt(100);
               print(monsterEncounter);
               if (monsterEncounter>=2) {
               print("Out pops a goblin from a nearby bush!");
               print("The goblin goes in for a attack!");
               print("Do you want to fight or run?");
               currentOption = scan.next();
               if (currentOption ==("fight")) {
               fight(currentOption);
               print("After getting away from the goblin you notice a small cave nearby");
               }

                 else if (currentOption ==("run")) {
                        runAway(currentOption);
                        print("After getting away from the goblin you notice a small cave nearby");
                 }
                 else if (monsterEncounter<=1) {
                         print("You check the bush and find a magic pile of money along with a silver key");
                         setGold (gold + 20);
                         print("You found 20 gold inside the bag, you now have "+ getGold() +" pieces");
                         print("You notice a cave up ahead");
                  }
                 }
            print("Do you want to enter the cave?");
            currentOption = scan.next();
               if (currentOption ==("yes")) {
                  print("You enter the cave");
                  print("Out pops another goblin!");
                  print("Do you want to fight or run?");
                  currentOption = scan.next();
                  if (currentOption ==("fight")) {
               fight(currentOption);
               print("After defeating the goblin you search the cave and find some treasure!");
               setGold(gold + 15);
               print("You found 15 gold!");
               print("You exit the cave and continue on the trail");
               }

                 else if (currentOption ==("run")) {
                        runAway(currentOption);
                        print("You ran away from the goblin and escaped the cave!");
                        print("You continue to follow the trail");
                 }

                     }
              else if (currentOption ==("No")) {
              print("You continue on the trail and ignore the cave!");
              }
              print("While following the trail you find two routes to take, one up a dangerous cliff, and the other is a more safe path, which one would you like to take? Cliff or Path");

              currentOption = scan.next();

              if (currentOption ==("Path")) {
              print("You choose to go the safe route, but while following the path a bandit suprises you and charges in for a attack!");
              print("Do you want to run or fight?");
               if (currentOption ==("Run")) {
                  runAway(currentOption);
                  }
                  else if (currentOption ==("Fight")) {
                  fight(currentOption);
                  }
                }
               else if (currentOption ==("Cliff")) {
               int climb = rand.nextInt(10);
                  while (climb<=5) {
                  print("You attempted to climb the cliff but fell!");
                  climb = climb + 1;
                  healthLoss = rand.nextInt(5);
                  setHealth (health - healthLoss);
                  print("You lost "+ healthLoss +" health from the fall!");
                     if (getHealth()<=0) {
                     System.exit(0);
                     }
                  }
                  print("You succsesfully climbed the cliff!");
               }
               print("When you reach the top of the cliff you see a small village, do you want to enter the village? (this will be your last time to shop)");
               currentOption = scan.next();

        if (currentOption ==("Yes")) {
            print("You notice that there's a few shops after entering the village.");
            print("You see a potion shop, a weapons shop, and an armor shop. Would you like to go to one? Y/N");
            currentOption = scan.next();



            while (currentOption ==("Yes")) {
               print("Which shop would you like to go to?");
               openShop(currentOption = scan.next());
               print("Would you like to go to another shop? Y/N");
               currentOption = scan.next();
               }
               }
           else if (currentOption ==("No")) {
           print("You decide not to go into the village and continue following the path");
           }
           print("You continue to follow the path and finally reach the top of the mountain");


          }// this is the bracket to end main method

        private static void openShop (String currentOption){
            if (currentOption ==("potion")) {
                //case "potion":
                    print("You walk into the potion shop and notice there's a few items that catch your interest");
                    print("Health+2: 10G \nStrength+2: 10G");
                    print("Would you like to buy one?");
                    currentOption = scan.next();
                    if (currentOption ==("health")) {
                        print("You walk up to the shop owner and point at the small red flask, the shop owner gives a disgruntled look and tries to take 15 gold");
                        if (getGold() >= 15) {   // health NEEDS TO GO INTO ARRAY
                            setGold(gold - 15);
                            print(" The shop keeper takes 15 gold from you and hands you the potion");
                            print("You now have " + getGold() + " gold pieces");
                            setPotion("health");
                            print("You now have a " + getPotion() + " potion");
                            print("Be careful you can only have one potion at a time");
                            print("You exit the shop, would you like to go the weapon or armor shop, or leave town");
                        } // strength potion NEEDS TO GO INTO ARRAY
                    } else if (currentOption ==("Strength")) {
                        print("You walk up to the shop owner and point at the small green flask, the shop owner gives a disgruntled look and tries to take 10 gold");
                        if (getGold() >= 10) {
                            setGold(gold - 10);
                            print("The shop keeper takes 10 gold from you and hands you the potion");
                            print("You now have " + getGold() + " gold pieces");
                            setPotion("strength");
                            print("You now have a " + getPotion() + " potion");
                            print("Be careful you can only have one potion at a time");
                            print("You exit the shop, would you like to go the weapon or armor shop, or leave town");
                        }
                    }
                    else {
                    print("The shop owner doesnt understand you and points you towards the exit");
                    print("You exit the shop, would you like to go the weapon or armor shop, or leave town");
                    }
                   }
                 //   break;
                        //case "weapon":
                        if (currentOption ==("weapon")) {
                        print("You walk into the weapon shop and notice there's a few items that catch your interest");
                        print(" Sword+3: 15G \nAxe+5: 20G");
                        print(" Which one would you like to buy one");
                        currentOption = scan.next();
                           if (currentOption ==("Sword")) {
                           // prevents stacking dmg HOW WOULD I PUT THIS INTO A ARRAY
                           setWeaponDmg (weaponDmg - weaponDmg);
                              print("You point at the sword and the shop keeper tries to take 15 gold");
                                 if (getGold() >=15) {
                                 setGold (gold - 15);
                                 print("The shop keeper takes 15 gold from you and hands you the sword");
                                 print("You now have "+ getGold() +" gold pieces");
                                 setWeaponDmg (weaponDmg + 3);
                                 print(" You now deal a extra "+ getWeaponDmg() +" damage!");
                                 print("You exit the shop, would you like to go the potion or armor shop, or leave town");
                                 }
                                 else {
                                 print("You dont have enough gold for that, now get out!");
                                 print("You exit the shop, would you like to go the potion or armor shop, or leave town");
                                 }
                                }

                                if (currentOption ==("Axe")) {
                           // prevents stacking dmg HOW WOULD I PUT THIS INTO A ARRAY
                           setWeaponDmg (weaponDmg - weaponDmg);
                              print("You point at the Axe and the shop keeper tries to take 20 gold");
                                 if (getGold() >=20) {
                                 setGold (gold - 20);
                                 print("The shop keeper takes 20 gold from you and hands you the axe");
                                 print("You now have "+ getGold() +" gold pieces");
                                 setWeaponDmg (weaponDmg + 5);
                                 print(" You now deal a extra "+ getWeaponDmg() +" damage!");
                                 print("You exit the shop, would you like to go the potion or armor shop, or leave town");
                                 }
                                 else {
                                 print("You dont have enough gold for that, now get out!");
                                 print("You exit the shop, would you like to go the potion or armor shop, or leave town");
                                 }
                                }
                               }
               //     break;
                         //case "armor":
                         if (currentOption ==("armor")) {
                        print("You walk into the weapon shop and notice there's a few items that catch your interest");
                        print(" Leather Armor+5: 20G \nIron Armor+10: 25G");
                        print(" Which one would you like to buy one");
                        currentOption = scan.next();
                         if (currentOption ==("Leather")) {
                          print("You point at the Leather Armor and the shop keeper tries to take 20 gold");
                          if (getGold() >=20) {
                          setGold (gold - 20);
                          print("The shop keeper takes 20 gold from you and hands you the armor");
                          setHealth (health + 5);
                          print("You now have "+ getHealth() +" Health");
                          print("You exit the shop, would you like to go the potion or weapon shop, or leave town");
                          }
                          else {
                           print("You dont have enough gold for that, now get out!");
                           print("You exit the shop, would you like to go the potion or weapon shop, or leave town");
                           }
                          }
                          if (currentOption ==("Iron")) {
                          print("You point at the Iron Armor and the shop keeper tries to take 25 gold");
                          if (getGold() >=25) {
                          setGold (gold - 25);
                          print("The shop keeper takes 25 gold from you and hands you the armor");
                          setHealth (health + 10);
                          print("You now have "+ getHealth() +" Health");
                          print("You exit the shop, would you like to go the potion or weapon shop, or leave town");
                          }
                          else {
                           print("You dont have enough gold for that, now get out!");
                           print("You exit the shop, would you like to go the potion or weapon shop, or leave town");
                           }
                          }
                         }
               //     break;
               /* default:
                  print("You look to yourself confused");
                    break; */
            }

    private static void runAway (String currentOption) {
                           int goldLost = rand.nextInt(20);
                           int healthLoss = rand.nextInt(20);
                           setPoints(getPoints() - 10);
                           setMorale(getMorale() - 10);
                           print("You attempt to run away!");
                           int runChance = rand.nextInt(5);
                              if (runChance <= 5) {
                                  healthLoss = rand.nextInt(5);
                                  setHealth(health - healthLoss);
                                  setGold(getGold() - goldLost);
                            print("You lost " + healthLoss + " health and " + goldLost + " gold while trying to run away!");
                                 }
                            else {
                            print("You were able to escape without losing anything!");
                          } }
    private static void fight (String currentOption) {
                              potionDrink(currentOption);
                              int monsterHealth = rand.nextInt(10) * (getLevel() + 1);
                              while (monsterHealth>0)
                                    {
                                   int monsterDamage = rand.nextInt(5) * (getLevel() + 1);
                                   monsterDamage = monsterDamage + 1;
                                    if (monsterDamage>=4) {
                                    print("The monster hits you for "+ monsterDamage +" damage!");
                                    setHealth (health - monsterDamage);
                                       if (getHealth() <=0)
                                          {
                                          print("You died to the monsters attack!");
                                          System.exit(0);
                                                            }
                                            }
                                      // monster attack    miss
                                     else if (monsterDamage<2)
                                              {
                                              print("The monster attempts to attack but misses!");
                                              }
                                              //player attack
                                                    print("You attempt to attack the monster!");
                                                    int attackDmg = rand.nextInt(5);
                                                    attackDmg = attackDmg + getWeaponDmg();
                                                    if (attackDmg>=2) {
                                                       monsterHealth = (monsterHealth - attackDmg);
                                                      print("You hit the monster with "+ attackDmg +" points of damage!");
                                                                       }
                                                     //check if monster died
                                                   if (monsterHealth<=0) {
                                                   print("You killed the monster!");
                                                   int goldAdd = rand.nextInt(15);
                                                   int pointAdd = rand.nextInt(10);
                                                   setPoints (points + pointAdd);
                                                   setGold (gold + goldAdd);
                                                   print("You gained "+ goldAdd +" gold, you now have "+ getGold() +" gold pieces");
                                                   print("You gained "+ pointAdd +" experience, you now have "+ getPoints() +" experience points");
                                                   print("You now have "+ getHealth() +" hit points");
                                                   levelUp();
                                                      }
                                                   else if (attackDmg<=1){
                                                   print("You missed your attack!");
                                                   }
                     }// end to loop
             }

    private static void levelUp() {
      int levelPass = 10;
         if (getPoints() >= levelPass) {
         setHealth (health + 10);
         setWeaponDmg (weaponDmg + 1);
         setPoints (points - levelPass);
         levelPass = (levelPass + 10);
         setLevel (level + 1);
         print("You leveled up!");
         print("You are now "+ getLevel() +"!");
         print("You gained 10 hit points!");
         print("You now deal 1 extra damage!");
      }
    }
    private static void potionDrink(String currentOption) {
                     print("Do you want to drink a potion before the fight?");
                     currentOption = scan.next();
                     if (currentOption ==("yes")) {
                     if (getPotion() ==("Health")) {
                     print("You quickly drink the health potion and gain 2 health");
                     setHealth (health+2);
                     }
                     else if (getPotion() ==("Strength")) {
                     print("You quickly drink the strength potion and gain 2 attack damage!");
                     setWeaponDmg (weaponDmg + 2);
                     }
                  }
                  else if  (currentOption ==("no"))  {
                  print("");
                  }
                  else if (getPotion() ==("Potion")) {
                   print("");
                  }
               }

    private static int getPoints() {
        return points;
    }
    private static int getLevel() {
    return level;
    }
    private static int getGold() {
        return gold;
    }

    private static int getHealth() {
        return health;
    }

    private static int getMorale() {
        return morale;
    }

    private static int getWeaponDmg() {
        return weaponDmg;
    }
    private static String getPotion() {
        return Potion;
    }

    private static void setPotion(String potion) {
        Potion = potion;
    }

    private static void setPoints(int newPoints) {
    points = newPoints;
    }
   private static void setLevel(int newLevel) {
   level = newLevel;
   }
    private static void setGold(int newGold) {
        gold = newGold;
    }

    private static void setHealth(int newHealth) {
        health = newHealth;
    }

    private static void setMorale(int newMorale) {
        morale = newMorale;
    }

    private static void setWeaponDmg(int newWeaponDmg) {
        weaponDmg = newWeaponDmg;
    }
}