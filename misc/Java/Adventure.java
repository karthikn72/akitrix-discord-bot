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
         
        System.out.println("You have " + getPoints() + " points, this will be your levelling system, do you understand? Y/N"); 
        currentOption = scan.next();
 
        if (currentOption.equalsIgnoreCase("Yes")) {
            System.out.println("You may continue with your adventure!");
        } else {
            System.out.println("We're going to continue anyways.");
        }
        System.out.println("While walking through the woods something jumps out of the bushes!");
        System.out.println("Its a wild boar, and it doesnt look happy!");
        System.out.println("Do you want to run or fight?");

        currentOption = scan.next();
             if (currentOption.equalsIgnoreCase("fight")) {
               fight(currentOption);
               }  
               
                 else if (currentOption.equalsIgnoreCase("run")) {
                        runAway(currentOption);
                 }

            
            
            System.out.println("You notice there is a village up ahead...");
            System.out.println("Do you want to go to the village? (Y/N)");
            currentOption = scan.next();
        
        if (currentOption.equalsIgnoreCase("Yes")) {
            System.out.println("You notice that there's a few shops after entering the village.");
            System.out.println("You see a potion shop, a weapons shop, and an armor shop. Would you like to go to one? Y/N");
            currentOption = scan.next();
            
            while (currentOption.equalsIgnoreCase("Yes")) {
               System.out.println("Which shop would you like to go to?");
               openShop(currentOption = scan.next());
               System.out.println("Would you like to go to another shop? Y/N");
               currentOption = scan.next();
               }
              
              System.out.println("You begin to leave the town and notice a bounty board for hunting down a monster");
              System.out.println("You decide to take up this task on defeating the monster and set out into the woods");
              }
              else if (currentOption.equalsIgnoreCase("No")){
              System.out.println("You decide to continue traveling through the woods");
              }
              System.out.println("While in the woods you begin to here a rustling noise");
               monsterEncounter = rand.nextInt(100);
               System.out.println(monsterEncounter);
               if (monsterEncounter>=2) {
               System.out.println("Out pops a goblin from a nearby bush!");
               System.out.println("The goblin goes in for a attack!");
               System.out.println("Do you want to fight or run?");
               currentOption = scan.next();
               if (currentOption.equalsIgnoreCase("fight")) {
               fight(currentOption);
               System.out.println("After getting away from the goblin you notice a small cave nearby");
               }  
               
                 else if (currentOption.equalsIgnoreCase("run")) {
                        runAway(currentOption);
                        System.out.println("After getting away from the goblin you notice a small cave nearby");
                 }
                 else if (monsterEncounter<=1) {
                         System.out.println("You check the bush and find a magic pile of money along with a silver key");
                         setGold (gold + 20);
                         System.out.println("You found 20 gold inside the bag, you now have "+ getGold() +" pieces");
                         System.out.println("You notice a cave up ahead");
                  }
                 }
            System.out.println("Do you want to enter the cave?");
            currentOption = scan.next();
               if (currentOption.equalsIgnoreCase("yes")) {
                  System.out.println("You enter the cave");
                  System.out.println("Out pops another goblin!");
                  System.out.println("Do you want to fight or run?");
                  currentOption = scan.next();
                  if (currentOption.equalsIgnoreCase("fight")) {
               fight(currentOption);
               System.out.println("After defeating the goblin you search the cave and find some treasure!");
               setGold(gold + 15);
               System.out.println("You found 15 gold!");
               System.out.println("You exit the cave and continue on the trail");
               }  
               
                 else if (currentOption.equalsIgnoreCase("run")) {
                        runAway(currentOption);
                        System.out.println("You ran away from the goblin and escaped the cave!");
                        System.out.println("You continue to follow the trail");
                 }
                       
                     } 
              else if (currentOption.equalsIgnoreCase("No")) {
              System.out.println("You continue on the trail and ignore the cave!");
              }
              System.out.println("While following the trail you find two routes to take, one up a dangerous cliff, and the other is a more safe path, which one would you like to take? Cliff or Path");
              
              currentOption = scan.next();
              
              if (currentOption.equalsIgnoreCase("Path")) {
              System.out.println("You choose to go the safe route, but while following the path a bandit suprises you and charges in for a attack!");
              System.out.println("Do you want to run or fight?");
               if (currentOption.equalsIgnoreCase("Run")) {
                  runAway(currentOption);
                  }
                  else if (currentOption.equalsIgnoreCase("Fight")) {
                  fight(currentOption);
                  }
                }
               else if (currentOption.equalsIgnoreCase("Cliff")) {
               int climb = rand.nextInt(10);
                  while (climb<=5) {
                  System.out.println("You attempted to climb the cliff but fell!");
                  climb = climb + 1;
                  healthLoss = rand.nextInt(5);
                  setHealth (health - healthLoss);
                  System.out.println("You lost "+ healthLoss +" health from the fall!");
                     if (getHealth()<=0) {
                     System.exit(0);
                     }
                  }
                  System.out.println("You succsesfully climbed the cliff!");
               }
               System.out.println("When you reach the top of the cliff you see a small village, do you want to enter the village? (this will be your last time to shop)");
               currentOption = scan.next();
        
        if (currentOption.equalsIgnoreCase("Yes")) {
            System.out.println("You notice that there's a few shops after entering the village.");
            System.out.println("You see a potion shop, a weapons shop, and an armor shop. Would you like to go to one? Y/N");
            currentOption = scan.next();
               
            
            
            while (currentOption.equalsIgnoreCase("Yes")) {
               System.out.println("Which shop would you like to go to?");
               openShop(currentOption = scan.next());
               System.out.println("Would you like to go to another shop? Y/N");
               currentOption = scan.next();
               }
               }
           else if (currentOption.equalsIgnoreCase("No")) {
           System.out.println("You decide not to go into the village and continue following the path");
           }
           System.out.println("You continue to follow the path and finally reach the top of the mountain");
               
                          
          }// this is the bracket to end main method
            
        private static void openShop (String currentOption){
            if (currentOption.equalsIgnoreCase("potion")) {
                //case "potion":
                    System.out.println("You walk into the potion shop and notice there's a few items that catch your interest");
                    System.out.println("Health+2: 10G \nStrength+2: 10G");
                    System.out.println("Would you like to buy one?");
                    currentOption = scan.next();
                    if (currentOption.equalsIgnoreCase("health")) {
                        System.out.println("You walk up to the shop owner and point at the small red flask, the shop owner gives a disgruntled look and tries to take 15 gold");
                        if (getGold() >= 15) {   // health NEEDS TO GO INTO ARRAY
                            setGold(gold - 15);
                            System.out.println(" The shop keeper takes 15 gold from you and hands you the potion");
                            System.out.println("You now have " + getGold() + " gold pieces");
                            setPotion("health");
                            System.out.println("You now have a " + getPotion() + " potion");
                            System.out.println("Be careful you can only have one potion at a time");
                            System.out.println("You exit the shop, would you like to go the weapon or armor shop, or leave town");
                        } // strength potion NEEDS TO GO INTO ARRAY
                    } else if (currentOption.equalsIgnoreCase("Strength")) {
                        System.out.println("You walk up to the shop owner and point at the small green flask, the shop owner gives a disgruntled look and tries to take 10 gold");
                        if (getGold() >= 10) {
                            setGold(gold - 10);
                            System.out.println("The shop keeper takes 10 gold from you and hands you the potion");
                            System.out.println("You now have " + getGold() + " gold pieces");
                            setPotion("strength");
                            System.out.println("You now have a " + getPotion() + " potion");
                            System.out.println("Be careful you can only have one potion at a time");
                            System.out.println("You exit the shop, would you like to go the weapon or armor shop, or leave town");
                        }
                    }
                    else {
                    System.out.println("The shop owner doesnt understand you and points you towards the exit");
                    System.out.println("You exit the shop, would you like to go the weapon or armor shop, or leave town");
                    }
                   }
                 //   break;
                        //case "weapon": 
                        if (currentOption.equalsIgnoreCase("weapon")) {
                        System.out.println("You walk into the weapon shop and notice there's a few items that catch your interest");
                        System.out.println(" Sword+3: 15G \nAxe+5: 20G");
                        System.out.println(" Which one would you like to buy one");
                        currentOption = scan.next();
                           if (currentOption.equalsIgnoreCase("Sword")) {
                           // prevents stacking dmg HOW WOULD I PUT THIS INTO A ARRAY
                           setWeaponDmg (weaponDmg - weaponDmg);
                              System.out.println("You point at the sword and the shop keeper tries to take 15 gold");
                                 if (getGold() >=15) {
                                 setGold (gold - 15);
                                 System.out.println("The shop keeper takes 15 gold from you and hands you the sword");
                                 System.out.println("You now have "+ getGold() +" gold pieces");
                                 setWeaponDmg (weaponDmg + 3);
                                 System.out.println(" You now deal a extra "+ getWeaponDmg() +" damage!");
                                 System.out.println("You exit the shop, would you like to go the potion or armor shop, or leave town"); 
                                 } 
                                 else {
                                 System.out.println("You dont have enough gold for that, now get out!");
                                 System.out.println("You exit the shop, would you like to go the potion or armor shop, or leave town"); 
                                 } 
                                }
                               
                                if (currentOption.equalsIgnoreCase("Axe")) {
                           // prevents stacking dmg HOW WOULD I PUT THIS INTO A ARRAY
                           setWeaponDmg (weaponDmg - weaponDmg);
                              System.out.println("You point at the Axe and the shop keeper tries to take 20 gold");
                                 if (getGold() >=20) {
                                 setGold (gold - 20);
                                 System.out.println("The shop keeper takes 20 gold from you and hands you the axe");
                                 System.out.println("You now have "+ getGold() +" gold pieces");
                                 setWeaponDmg (weaponDmg + 5);
                                 System.out.println(" You now deal a extra "+ getWeaponDmg() +" damage!");
                                 System.out.println("You exit the shop, would you like to go the potion or armor shop, or leave town"); 
                                 }
                                 else {
                                 System.out.println("You dont have enough gold for that, now get out!");
                                 System.out.println("You exit the shop, would you like to go the potion or armor shop, or leave town"); 
                                 }
                                }
                               }
               //     break;
                         //case "armor":
                         if (currentOption.equalsIgnoreCase("armor")) {
                        System.out.println("You walk into the weapon shop and notice there's a few items that catch your interest");
                        System.out.println(" Leather Armor+5: 20G \nIron Armor+10: 25G");
                        System.out.println(" Which one would you like to buy one");
                        currentOption = scan.next();
                         if (currentOption.equalsIgnoreCase("Leather")) {
                          System.out.println("You point at the Leather Armor and the shop keeper tries to take 20 gold");
                          if (getGold() >=20) {
                          setGold (gold - 20);
                          System.out.println("The shop keeper takes 20 gold from you and hands you the armor");
                          setHealth (health + 5);
                          System.out.println("You now have "+ getHealth() +" Health");
                          System.out.println("You exit the shop, would you like to go the potion or weapon shop, or leave town"); 
                          }
                          else {
                           System.out.println("You dont have enough gold for that, now get out!");
                           System.out.println("You exit the shop, would you like to go the potion or weapon shop, or leave town"); 
                           }
                          }
                          if (currentOption.equalsIgnoreCase("Iron")) {
                          System.out.println("You point at the Iron Armor and the shop keeper tries to take 25 gold");
                          if (getGold() >=25) {
                          setGold (gold - 25);
                          System.out.println("The shop keeper takes 25 gold from you and hands you the armor");
                          setHealth (health + 10);
                          System.out.println("You now have "+ getHealth() +" Health");
                          System.out.println("You exit the shop, would you like to go the potion or weapon shop, or leave town");             
                          }
                          else {
                           System.out.println("You dont have enough gold for that, now get out!");
                           System.out.println("You exit the shop, would you like to go the potion or weapon shop, or leave town"); 
                           }
                          }
                         }
               //     break;
               /* default:
                  System.out.println("You look to yourself confused");
                    break; */
            }
        
    private static void runAway (String currentOption) {
                           int goldLost = rand.nextInt(20);
                           int healthLoss = rand.nextInt(20);
                           setPoints(getPoints() - 10);
                           setMorale(getMorale() - 10);
                           System.out.println("You attempt to run away!");
                           int runChance = rand.nextInt(5);
                              if (runChance <= 5) {
                                  healthLoss = rand.nextInt(5);
                                  setHealth(health - healthLoss);
                                  setGold(getGold() - goldLost);
                            System.out.println("You lost " + healthLoss + " health and " + goldLost + " gold while trying to run away!");
                                 }
                            else {
                            System.out.println("You were able to escape without losing anything!");
                          } } 
    private static void fight (String currentOption) {
                              potionDrink(currentOption);
                              int monsterHealth = rand.nextInt(10) * (getLevel() + 1);
                              while (monsterHealth>0)
                                    {
                                   int monsterDamage = rand.nextInt(5) * (getLevel() + 1);
                                   monsterDamage = monsterDamage + 1;
                                    if (monsterDamage>=4) {
                                    System.out.println("The monster hits you for "+ monsterDamage +" damage!");
                                    setHealth (health - monsterDamage);
                                       if (getHealth() <=0)
                                          {
                                          System.out.println("You died to the monsters attack!");  
                                          System.exit(0);
                                                            }
                                            }
                                      // monster attack    miss  
                                     else if (monsterDamage<2)
                                              {
                                              System.out.println("The monster attempts to attack but misses!");
                                              }
                                              //player attack
                                                    System.out.println("You attempt to attack the monster!");
                                                    int attackDmg = rand.nextInt(5);
                                                    attackDmg = attackDmg + getWeaponDmg();
                                                    if (attackDmg>=2) {
                                                       monsterHealth = (monsterHealth - attackDmg);
                                                      System.out.println("You hit the monster with "+ attackDmg +" points of damage!");
                                                                       }      
                                                     //check if monster died                    
                                                   if (monsterHealth<=0) {
                                                   System.out.println("You killed the monster!");
                                                   int goldAdd = rand.nextInt(15);
                                                   int pointAdd = rand.nextInt(10);
                                                   setPoints (points + pointAdd);
                                                   setGold (gold + goldAdd);
                                                   System.out.println("You gained "+ goldAdd +" gold, you now have "+ getGold() +" gold pieces");
                                                   System.out.println("You gained "+ pointAdd +" experience, you now have "+ getPoints() +" experience points");
                                                   System.out.println("You now have "+ getHealth() +" hit points");
                                                   levelUp();
                                                      }
                                                   else if (attackDmg<=1){
                                                   System.out.println("You missed your attack!");
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
         System.out.println("You leveled up!");
         System.out.println("You are now "+ getLevel() +"!");
         System.out.println("You gained 10 hit points!");
         System.out.println("You now deal 1 extra damage!"); 
      }
    }
    private static void potionDrink(String currentOption) {
                     System.out.println("Do you want to drink a potion before the fight?");
                     currentOption = scan.next();
                     if (currentOption.equalsIgnoreCase("yes")) {
                     if (getPotion().equalsIgnoreCase("Health")) {
                     System.out.println("You quickly drink the health potion and gain 2 health");
                     setHealth (health+2);
                     }
                     else if (getPotion().equalsIgnoreCase("Strength")) {
                     System.out.println("You quickly drink the strength potion and gain 2 attack damage!");
                     setWeaponDmg (weaponDmg + 2);
                     }
                  }
                  else if  (currentOption.equalsIgnoreCase("no"))  {
                  System.out.println("");
                  }
                  else if (getPotion().equalsIgnoreCase("Potion")) {
                   System.out.println("");
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